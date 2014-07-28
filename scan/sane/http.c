/************************************************************************************\
  http.c - HTTP/1.1 feeder and consumer

  (c) 2008 Copyright Hewlett-Packard Development Company, LP

  Permission is hereby granted, free of charge, to any person obtaining a copy 
  of this software and associated documentation files (the "Software"), to deal 
  in the Software without restriction, including without limitation the rights 
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
  of the Software, and to permit persons to whom the Software is furnished to do 
  so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

  In order to support state-less connections, each HTTP/1.1 connection or session 
  must start with http_open and end with http_close. 

  Author: Naga Samrat Chowdary, Narla
  Contributing Author: Sarbeswar Meher
\************************************************************************************/

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <ctype.h>
#include "hpmud.h"
#include "http.h"

//#define HTTP_DEBUG

#define _STRINGIZE(x) #x
#define STRINGIZE(x) _STRINGIZE(x)

#define BUG(args...) syslog(LOG_ERR, __FILE__ " " STRINGIZE(__LINE__) ": " args)

#ifdef HTTP_DEBUG
   #define DBG(args...) syslog(LOG_INFO, __FILE__ " " STRINGIZE(__LINE__) ": " args)
   #define DBG_DUMP(data, size) sysdump((data), (size))
   #define DBG_SZ(args...) syslog(LOG_INFO, args)
#else
   #define DBG(args...)
   #define DBG_DUMP(data, size)
   #define DBG_SZ(args...)
#endif

#define EXCEPTION_TIMEOUT 45 /* seconds */

enum HTTP_STATE
{
   HS_ACTIVE = 1,
   HS_EOF,
};

struct stream_buffer
{
   char buf[4096];
   int index;
   int cnt;   
};

struct http_session
{
   enum HTTP_STATE state;
   int http_status;
   int footer;         /* current footer */
   int total;
   HPMUD_DEVICE dd;  /* hpiod device descriptor */
   HPMUD_CHANNEL cd;  /* hpiod soap channel descriptor */
   struct stream_buffer s;
};

#if 0
static char *strnstr(const char *haystack, const char *needle, size_t n)
{
   int i, len=strlen(needle);

   for (i=0; *haystack && i<n; ++haystack, i++)
   {
      if (strncmp(haystack, needle, len) == 0)
      {
         return ((char *)haystack);
      }
   }
   return 0;
}
#endif

#if 0
static void sysdump(const void *data, int size)
{
    /* Dump size bytes of *data. Output looks like:
     * [0000] 75 6E 6B 6E 6F 77 6E 20 30 FF 00 00 00 00 39 00 unknown 0.....9.
     */

    unsigned char *p = (unsigned char *)data;
    unsigned char c;
    int n;
    char bytestr[4] = {0};
    char addrstr[10] = {0};
    char hexstr[16*3 + 5] = {0};
    char charstr[16*1 + 5] = {0};
    for(n=1;n<=size;n++) {
        if (n%16 == 1) {
            /* store address for this line */
            snprintf(addrstr, sizeof(addrstr), "%.4d", (int)((p-(unsigned char *)data) & 0xffff));
        }
            
        c = *p;
        if (isprint(c) == 0) {
            c = '.';
        }

        /* store hex str (for left side) */
        snprintf(bytestr, sizeof(bytestr), "%02X ", *p);
        strncat(hexstr, bytestr, sizeof(hexstr)-strlen(hexstr)-1);

        /* store char str (for right side) */
        snprintf(bytestr, sizeof(bytestr), "%c", c);
        strncat(charstr, bytestr, sizeof(charstr)-strlen(charstr)-1);

        if(n%16 == 0) { 
            /* line completed */
            DBG_SZ("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
            hexstr[0] = 0;
            charstr[0] = 0;
        }
        p++; /* next byte */
    }

    if (strlen(hexstr) > 0) {
        /* print rest of buffer if not empty */
        DBG_SZ("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
    }
}
#endif

/* Read data into stream buffer. Return specified "size" or less. Unused data is left in the stream. */
static int read_stream(struct http_session *ps, char *data, int size, int sec_timeout, int *bytes_read)
{
   int len, stat=1;
   int tmo=sec_timeout;        /* initial timeout */
   int max=sizeof(ps->s.buf);
   enum HPMUD_RESULT ret;

   DBG("read_stream() ps=%p data=%p size=%d timeout=%d s.index=%d s.cnt=%d\n", ps, data, size, sec_timeout, ps->s.index, ps->s.cnt);

   *bytes_read = 0;

   /* Return any data in the stream first. */
   if (ps->s.cnt)
   {
      if (ps->s.cnt > size)
      {
         /* Return part of stream buffer. */
         len = size;
         memcpy(data, &ps->s.buf[ps->s.index], len);
         ps->s.index += len;
         ps->s.cnt -= len;
      }
      else
      {
         /* Return all of rbuf. */
         len = ps->s.cnt;
         memcpy(data, &ps->s.buf[ps->s.index], len);
         ps->s.index = ps->s.cnt = 0;       /* stream is empty reset */
      }
      *bytes_read = len;
      DBG("-read_stream() bytes_read=%d s.index=%d s.cnt=%d\n", len, ps->s.index, ps->s.cnt);
      return 0;
   }

   /* Stream is empty read more data from device. */
   ret = hpmud_read_channel(ps->dd, ps->cd, &ps->s.buf[ps->s.index], max-(ps->s.index + ps->s.cnt), tmo, &len);
   if (ret == HPMUD_R_IO_TIMEOUT)
   {
      BUG("timeout reading data sec_timeout=%d\n", tmo);
      goto bugout;
   }
   if (ret != HPMUD_R_OK)
   {
      BUG("read_stream error stat=%d\n", ret);
      goto bugout;
   }
   if (len==0)
   {
      BUG("read_stream error len=0\n");   /* shouldn't happen, but it does with jetdirect */
      goto bugout;
   }

   DBG("read_channel len=%d\n", len);
   ps->s.cnt += len;

   if (ps->s.cnt > size)
   {
      /* Return part of stream buffer. */
      len = size;
      memcpy(data, &ps->s.buf[ps->s.index], len);
      ps->s.index += len;
      ps->s.cnt -= len;
   }
   else
   {
      /* Return all of rbuf. */
      len = ps->s.cnt;
      memcpy(data, &ps->s.buf[ps->s.index], len);
      ps->s.index = ps->s.cnt = 0;       /* stream is empty reset */
   }

   *bytes_read = len;
   stat = 0;
   DBG("-read_stream() bytes_read=%d s.index=%d s.cnt=%d\n", len, ps->s.index, ps->s.cnt);

bugout:
   return stat;
}

static int read_char(struct http_session *ps, int sec_timeout)
{
   unsigned char ch;
   int len;
   if (read_stream(ps, (char *)&ch, 1, sec_timeout, &len))
      return -1;
   else
      return ch;  
}

/* Read a line of data. Line length is not known. */
static int read_line(struct http_session *ps, char *line, int line_size, int sec_timeout, int *bytes_read)
{
   int total=0, stat=1;
   int ch, cr=0, lf=0;
   int tmo=sec_timeout;        /* initial timeout */

   *bytes_read = 0;

   while (total < (line_size-1))
   {
      ch = read_char(ps, tmo);
      line[total++]=ch;

      if (ch == '\r')
         cr=1;
      else if (ch == '\n' && cr)
         break;   /* done, found CRLF */
      else if (ch == '\n' && lf)
         break;   /* done, found LFLF (for kiwi "501 Not Implemented") */
      else if (ch == '\n')
         lf=1;
      else if (ch == -1)
         goto bugout;  /* error */
      else
      {
        cr=0;
        lf=0;
      }
      tmo=3;  /* changed 1 to 3 for 1200dpi uncompressed, DES 8/20/08. */ 
   }
   stat = 0;

bugout:
   line[total]=0;
   *bytes_read=total;   /* length does not include null termination */
   DBG("read_line len=%d index=%d cnt=%d\n", total, ps->s.index, ps->s.cnt);
   return stat;
}

/* Http_open must be called for each HTTP/1.1 connection or session. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_open(HPMUD_DEVICE dd, const char *channel, HTTP_HANDLE *handle)
{
   struct http_session *ps;
   enum HTTP_RESULT stat = HTTP_R_IO_ERROR;
   
   DBG("http_open() dd=%d channel=%s handle=%p\n", dd, channel, handle);

   *handle = NULL;

   if ((ps = malloc(sizeof(struct http_session))) == NULL)
   {
      BUG("malloc failed: %m\n");
      return HTTP_R_MALLOC_ERROR;
   }
   memset(ps, 0, sizeof(struct http_session));

   ps->dd = dd;
   if (hpmud_open_channel(ps->dd, channel, &ps->cd) != HPMUD_R_OK)
   {
      BUG("unable to open %s channel\n", channel);
      goto bugout;
   }

   ps->state = HS_ACTIVE;
   *handle = ps;
   stat = HTTP_R_OK;

bugout:
   if (stat != HTTP_R_OK)
      free(ps);
   return stat;
}

/* Http_close must be called after the HTTP/1.1 connection closes. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_close(HTTP_HANDLE handle)
{
   struct http_session *ps = (struct http_session *)handle;
   DBG("http_close() handle=%p\n", handle);
   if (ps->cd > 0)
      hpmud_close_channel(ps->dd, ps->cd);
   free(ps);
   return HTTP_R_OK;
}

/* Read HTTP/1.1 header. Blocks until header is read or timeout. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_read_header(HTTP_HANDLE handle, void *data, int max_size, int sec_timeout, int *bytes_read)
{
   struct http_session *ps = (struct http_session *)handle;
   int len, total; 
   int tmo=sec_timeout;   /* set initial timeout */
   enum HTTP_RESULT stat = HTTP_R_IO_ERROR;

   DBG("http_read_header() handle=%p data=%p size=%d sectime=%d\n", handle, data, max_size, sec_timeout);

   *bytes_read = 0;

   /* Read initial HTTP/1.1 header status line. */
   if (read_line(ps, data, max_size, tmo, &len))
      goto bugout;
   ps->http_status = strtol(data+9, NULL, 10);
   *bytes_read = total = len;

   /* Check for good status, ignore 400 (no job id found for JobCancelRequest) */                    
   if (!((ps->http_status >= 200 && ps->http_status < 300) || ps->http_status == 400))
   {
      BUG("invalid http_status=%d\n", ps->http_status);

      /* Dump any outstanding payload here. */
      while (!read_stream(ps, data, max_size, 1, &len))
         BUG("dumping len=%d\n", len);
      goto bugout;                
   }

   /* Read rest of header. Look for blank line. */
   *bytes_read = total = len;
   while (len > 2)
   {
      if (read_line(ps, data+total, max_size-total, tmo, &len))
         goto bugout;
      total += len;
     *bytes_read += len;
        DBG("http_read_header data=%s len=%d total=%d\n", (char*)data+total, len, total);
   }
   stat = HTTP_R_OK;

   DBG("-http_read_header() handle=%p data=%p bytes_read=%d size=%d status=%d\n", handle, data, *bytes_read, max_size, stat);

bugout:
   return stat;
};

/* Reads data from HTTP/1.1 chunked data stream until EOF. Returns max_size or less. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_read_payload(HTTP_HANDLE handle, void *data, int max_size, int sec_timeout, int *bytes_read)
{
   struct http_session *ps = (struct http_session *)handle;
   char line[128];
   int len; 
   int tmo=sec_timeout;   /* set initial timeout */
   enum HTTP_RESULT stat = HTTP_R_IO_ERROR;

   DBG("http_read_payload() handle=%p data=%p size=%d sectime=%d\n", handle, data, max_size, sec_timeout);

   *bytes_read = 0;

   if (ps->state == HS_EOF)
   {
      stat = HTTP_R_EOF;
   }
   else
   {
      if (ps->footer)
      {
         /* Footer is not complete. Continue reading payload. */
         if (read_stream(ps, data, ps->footer < max_size ? ps->footer : max_size, tmo, &len))
            goto bugout;

         ps->total += len;
         ps->footer -= len;
         *bytes_read = len;

         if (ps->footer == 0)
            if (read_line(ps, line, sizeof(line), tmo, &len))   /* footer is complete, eat CRLF */
               goto bugout;

         stat = HTTP_R_OK;
      }
      else
      {
         /* Read new footer. */
         if (read_line(ps, line, sizeof(line), tmo, &len))
            goto bugout;
         ps->footer = strtol(line, NULL, 16);

         /* Check for zero footer. */
         if (ps->footer == 0)
         {
            /* Done eat blank line. */
            read_line(ps, line, sizeof(line), 1, &len);
            ps->state = HS_EOF;
            stat = HTTP_R_EOF;
         }
         else
         {
            /* Got a valid footer, continue reading payload. */
            if (read_stream(ps, data, ps->footer < max_size ? ps->footer : max_size, tmo, &len))
               goto bugout;

            ps->total += len;
            ps->footer -= len;
            *bytes_read = len;

            if (ps->footer == 0)
               if (read_line(ps, line, sizeof(line), tmo, &len))   /* footer is complete, eat CRLF */
                  goto bugout;

            stat = HTTP_R_OK;
         }
      }
   }  /* if (ps->state == HS_EOF) */

   DBG("-http_read_payload() handle=%p data=%p bytes_read=%d size=%d status=%d\n", handle, data, *bytes_read, max_size, stat);

bugout:
   return stat;
};

/* Reads data from HTTP/1.1 chunked data stream until EOF. Returns max_size or less. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_read(HTTP_HANDLE handle, void *data, int max_size, int sec_timeout, int *bytes_read)
{
   struct http_session *ps = (struct http_session *)handle;
   char line[128] ={0,};
   int len = 0, ret;
   int tmo=sec_timeout;   /* set initial timeout */
   enum HTTP_RESULT stat = HTTP_R_IO_ERROR;
   int total_payload_length=*bytes_read;

   DBG("http_read() handle=%p data=%p size=%d sectime=%d total_payload_length=%d\n", handle, data, max_size, sec_timeout, total_payload_length);

   ps->footer=total_payload_length;

   *bytes_read = 0;

      /* Read new footer. */
      if (ps->footer) //Payload length is known
      {
         while(ps->footer)
         {
              if (read_line(ps, line, sizeof(line), tmo, &len))
		       {
				 *bytes_read = (ps->footer) * (-1) + 12;
				    goto bugout; 
			   }
		     strcpy(data, line);
		     data=data+len;
		     ps->footer -= len;
            *bytes_read += len;
         }
      }	
      else
      {
         while(1)
         {
            ret = read_line (ps, line, sizeof(line), tmo, &len);
            *bytes_read += len;
            if(ret) //failed to read line 
		    {
		            ps->footer = 0;
		            break;
		    }
            strcpy(data, line);
            data = data + len;
            DBG("http_read len=%d datalen=%d data=%s\n", len, strlen((char*)data), (char*)data);
            //Check for the footer
            if (strncmp(data-7, ZERO_FOOTER, sizeof(ZERO_FOOTER)-1) == 0)
            {
               ps->footer = 0;
               break;
            }
         }//end while(1)
      }//end else
      stat = HTTP_R_OK;
      if(ps->footer == 0) stat=HTTP_R_EOF;

   DBG("-http_read() handle=%p data=%p bytes_read=%d size=%d status=%d\n", handle, data, *bytes_read, max_size, stat);

bugout:
   return stat;
};

enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_read_size(HTTP_HANDLE handle, void *data, int max_size, int sec_timeout, int *bytes_read)
{
  struct http_session *ps = (struct http_session *)handle;
  enum HTTP_RESULT stat = HTTP_R_IO_ERROR;

  if(ps && ps->state == HTTP_R_EOF) return HTTP_R_EOF;
  if(max_size == -1) 
  { 
    ps->state = HTTP_R_EOF; 
    return HTTP_R_EOF; 
  }

  DBG("http_read_size() handle=%p data=%p size=%d sectime=%d\n", handle, data, max_size, sec_timeout);

  *bytes_read=0;
  while(*bytes_read < max_size)
  {
    *((char*)data + (*bytes_read)) = read_char(ps, sec_timeout);
    *bytes_read = *bytes_read+1;
  }

  return stat = HTTP_R_OK;
}

/* Write data to HTTP/1.1 connection. Blocks until all data is written or timeout. Caller formats header, footer and payload. */
enum HTTP_RESULT __attribute__ ((visibility ("hidden"))) http_write(HTTP_HANDLE handle, void *data, int size, int sec_timeout)
{
   struct http_session *ps = (struct http_session *)handle;
   int len; 
   int tmo=sec_timeout;   /* set initial timeout */
   enum HTTP_RESULT stat = HTTP_R_IO_ERROR;

   DBG("http_write() handle=%p data=%p size=%d sectime=%d\n", handle, data, size, sec_timeout);

   if (hpmud_write_channel(ps->dd, ps->cd, data, size, tmo, &len) != HPMUD_R_OK)
   {
      BUG("unable to write channel data\n");
      goto bugout;
   }

   stat = HTTP_R_OK;

bugout:
   return stat;
}

void __attribute__ ((visibility ("hidden"))) http_unchunk_data(char *buffer)
{
  char *temp=buffer;
  char *p=buffer;
  int chunklen = 0;

  //Here buffer starts like "<?xml....". There is no chunklen, only buffer
  if (*p == '<')
  {
      while(*p)
      {
        if (!(*p == '\n' || *p == '\r' || *p =='\t'))
        {
         *temp = *p;
         temp++;
        }
        p++;
	  }
	  *temp = '\0';
	  return;
  }
  /*Here buffer looks like "chunklen data chunklen data 0"
  e.g "FE3 <?xml....  8E8 ... 0"*/
  while(1)
  {
    while(*p != '\n' && *p != '\r') 
    {
	 chunklen = chunklen << 4 ; //Multiply 16
	 if ('0' <= *p &&  *p<='9')
	   chunklen += *p - '0';
	 else if ('A' <= *p && *p <= 'F')
	    chunklen += 10  - 'A' + *p;
	 else if ('a' <= *p && *p <= 'f')
	    chunklen += 10 + *p - 'a';
	 else
	 {
	    chunklen = chunklen >> 4;
		break;
	 }
	 p++;
    }//end while()
    if (chunklen == 0)
       break ;
    while(*p == '\n' || *p == '\r' || *p =='\t') p++;
    //copy the data till chunklen
    while(chunklen > 0)
    {
	   if (!(*p == '\n' || *p == '\r' || *p =='\t'))
       {
        *temp = *p ;
        temp++;
       }
       p++;
       chunklen--;
    }
    while(*p == '\n' || *p == '\r' || *p =='\t') p++;
  }//end while(1)
  *temp = '\0';
}




