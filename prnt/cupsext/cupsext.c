/*
cupsext - Python extension class for CUPS 1.1+

(c) Copyright 2003-2007 Hewlett-Packard Development Company, L.P.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA


Portions based on:
"lpadmin" command for the Common UNIX Printing System (CUPS).

Copyright 1997-2003 by Easy Software Products.

These coded instructions, statements, and computer programs are the
property of Easy Software Products and are protected by Federal
copyright law.  Distribution and use rights are outlined in the file
"LICENSE.txt" which should have been included with this file.  If this
file is missing or damaged please contact Easy Software Products
at:

Attn: CUPS Licensing Information
Easy Software Products
44141 Airport View Drive, Suite 204
Hollywood, Maryland 20636-3111 USA

Voice: (301) 373-9603
EMail: cups-info@cups.org
  WWW: http://www.cups.org

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of Hewlett-Packard nor the names of its
contributors may be used to endorse or promote products derived
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PATENT INFRINGEMENT; PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Requires:
CUPS 1.1+
Python 2.2+

Author:
Don Welch
Yashwant Kumar Sahu

*/


#include <Python.h>
#include <structmember.h>
#include <cups/cups.h>
#include <cups/language.h>
#include <cups/ppd.h>

/* Ref: PEP 353 (Python 2.5) */
#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif

#if (CUPS_VERSION_MAJOR > 1) || (CUPS_VERSION_MINOR > 5)
    #define HAVE_CUPS_1_6 1
#endif

#ifndef HAVE_CUPS_1_6
    #define ippGetCount(attr)     attr->num_values
    #define ippGetGroupTag(attr)  attr->group_tag
    #define ippGetValueTag(attr)  attr->value_tag
    #define ippGetName(attr)      attr->name
    #define ippGetBoolean(attr, element) attr->values[element].boolean
    #define ippGetInteger(attr, element) attr->values[element].integer
    #define ippGetStatusCode(ipp) ipp->request.status.status_code
    #define ippGetString(attr, element, language) attr->values[element].string.text


    static ipp_attribute_t * ippFirstAttribute( ipp_t *ipp )
    {
        if (!ipp)
            return (NULL);
        return (ipp->current = ipp->attrs);
    }

    static ipp_attribute_t * ippNextAttribute( ipp_t *ipp )
    {
        if (!ipp || !ipp->current)
            return (NULL);
        return (ipp->current = ipp->current->next);
    }

    static int ippSetOperation( ipp_t *ipp, ipp_op_t op )
    {
        if (!ipp)
            return (0);
        ipp->request.op.operation_id = op;
        return (1);
    }

    static int ippSetRequestId( ipp_t *ipp, int request_id )
    {
        if (!ipp)
            return (0);
        ipp->request.any.request_id = request_id;
        return (1);
    }
#endif

static http_t * http = NULL;     /* HTTP object */

static http_t* acquireCupsInstance()
{
    if ( http == NULL)
    {
        http = httpConnectEncrypt( cupsServer(), ippPort(), cupsEncryption() );
    }

    return http;
}


PyObject * releaseCupsInstance( PyObject * self, PyObject * args )
{
    if (http)
    {
        httpClose(http);
    }
    
    http = NULL;
    return Py_BuildValue( "i", 1 );
}

int g_num_options = 0;
cups_option_t * g_options;

ppd_file_t * ppd = NULL;
cups_dest_t * dest = NULL;

cups_dest_t * g_dests = NULL;
int g_num_dests = 0;

static int auth_cancel_req = 0;    // 0--> authentication cancel is not requested, 1 --> authentication cancelled

const char * g_ppd_file = NULL;

/*
 * 'validate_name()' - Make sure the printer name only contains valid chars.
 */

static int                                /* O - 0 if name is no good, 1 if name is good */
validate_name( const char *name )         /* I - Name to check */
{
    return 1; // TODO: Make it work with utf-8 encoding
}

static PyObject * PyObj_from_UTF8(const char *utf8)
{
    PyObject *val = PyUnicode_Decode(utf8, strlen(utf8), "utf-8", NULL);

    if (!val)
    {
        // CUPS 1.2 always gives us UTF-8.  Before CUPS 1.2, the
        // ppd-* strings come straight from the PPD with no
        // transcoding, but the attributes-charset is still 'utf-8'
        // so we've no way of knowing the real encoding.
        // In that case, detect the error and force it to ASCII.
        char * ascii;
        const char * orig = utf8;
        int i;

        PyErr_Clear();
        ascii = malloc(1 + strlen (orig));

        for (i = 0; orig[i]; i++)
        {
            ascii[i] = orig[i] & 0x7f;
        }

        ascii[i] = '\0';
        val = PyString_FromString( ascii );
        free( ascii );
    }

    return val;
}

void debug(const char * text)
{
    char buf[4096];
    sprintf( buf, "print '%s'", text);
    PyRun_SimpleString( buf );

}

staticforward PyTypeObject printer_Type;

#define printerObject_Check(v) ((v)->ob_type == &printer_Type)

typedef struct
{
    PyObject_HEAD
    PyObject * device_uri;
    PyObject * printer_uri;
    PyObject * name;
    PyObject * location;
    PyObject * makemodel;
    PyObject * info;
    int accepting;
    int state;
}
printer_Object;


static void printer_dealloc( printer_Object * self )
{

    Py_XDECREF( self->name );
    Py_XDECREF( self->device_uri );
    Py_XDECREF( self->printer_uri );
    Py_XDECREF( self->location );
    Py_XDECREF( self->makemodel );
    Py_XDECREF( self->info );
    PyObject_DEL( self );
}


static PyMemberDef printer_members[] =
{
    { "device_uri", T_OBJECT_EX, offsetof( printer_Object, device_uri ), 0, "Device URI (device-uri)" },
    { "printer_uri", T_OBJECT_EX, offsetof( printer_Object, printer_uri ), 0, "Printer URI (printer-uri)" },
    { "name", T_OBJECT_EX, offsetof( printer_Object, name ), 0, "Name (printer-name)" },
    { "location", T_OBJECT_EX, offsetof( printer_Object, location ), 0, "Location (printer-location)" },
    { "makemodel", T_OBJECT_EX, offsetof( printer_Object, makemodel ), 0, "Make and model (printer-make-and-model)" },
    { "state", T_INT, offsetof( printer_Object, state ), 0, "State (printer-state)" },
    { "info", T_OBJECT_EX, offsetof( printer_Object, info ), 0, "Info/description (printer-info)" },
    { "accepting", T_INT, offsetof( printer_Object, accepting ), 0, "Accepting/rejecting" },
    {0}
};

static PyTypeObject printer_Type =
{
    PyObject_HEAD_INIT( &PyType_Type )
    0,                                     /* ob_size */
    "cupsext.Printer",                   /* tp_name */
    sizeof( printer_Object ),              /* tp_basicsize */
    0,                                     /* tp_itemsize */
    ( destructor ) printer_dealloc,           /* tp_dealloc */
    0,                                     /* tp_print */
    0,                                     /* tp_getattr */
    0,                                     /* tp_setattr */
    0,                                     /* tp_compare */
    0,                                     /* tp_repr */
    0,                                     /* tp_as_number */
    0,                                     /* tp_as_sequence */
    0,                                     /* tp_as_mapping */
    0,                                     /* tp_hash */
    0,                                     /* tp_call */
    0,                                     /* tp_str */
    PyObject_GenericGetAttr,               /* tp_getattro */
    PyObject_GenericSetAttr,               /* tp_setattro */
    0,                                     /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,         /* tp_flags */
    "CUPS Printer object",                 /* tp_doc */
    0,                                     /* tp_traverse */
    0,                                     /* tp_clear */
    0,                                     /* tp_richcompare */
    0,                                     /* tp_weaklistoffset */
    0,                                     /* tp_iter */
    0,                                     /* tp_iternext */
    0,         /*job_methods, */           /* tp_methods */
    printer_members,                       /* tp_members */
    0,                                     /* tp_getset */
    0,                                     /* tp_base */
    0,                                     /* tp_dict */
    0,                                     /* tp_descr_get */
    0,                                     /* tp_descr_set */
    0,                                     /* tp_dictoffset */
    0,                                     /* tp_init */
    0,                                     /* tp_alloc */
    0,                                     /* tp_new */
};




static PyObject * _newPrinter( char * device_uri,
                               char * name,
                               char * printer_uri,
                               char * location,
                               char * makemodel,
                               char * info,
                               int state,
                               int accepting )
{
    printer_Object * self = PyObject_New( printer_Object, &printer_Type );

    if ( !self )
        return NULL;

    if ( device_uri != NULL )
        self->device_uri = Py_BuildValue( "s", device_uri );

    if ( printer_uri != NULL )
        self->printer_uri = Py_BuildValue( "s", printer_uri );

    if ( name != NULL )
        self->name = Py_BuildValue( "s", name );

    if ( location != NULL )
        self->location = Py_BuildValue( "s", location );

    if ( makemodel != NULL )
        self->makemodel = Py_BuildValue( "s", makemodel );

    if ( info != NULL )
        self->info = Py_BuildValue( "s", info );

    self->accepting = accepting;
    self->state = state;

    return ( PyObject * ) self;
}

static PyObject * newPrinter( PyObject * self, PyObject * args, PyObject * kwargs )
{
    char * device_uri = "";
    char * name = "";
    char * location = "";
    char * makemodel = "";
    int state = 0;
    char * printer_uri = "";
    char * info = "";
    int accepting = 0;

    char * kwds[] = { "device_uri", "name", "printer_uri", "location",
                      "makemodel", "info", "state", "accepting", NULL
                    };

    if ( !PyArg_ParseTupleAndKeywords( args, kwargs, "zz|zzzzii", kwds,
                                       &device_uri, &name, &printer_uri,
                                       &location, &makemodel, &info, &state,
                                       &accepting )        )
        return NULL;

    return _newPrinter( device_uri, printer_uri, name, location, makemodel, info, state, accepting);
}



PyObject * getPrinters( PyObject * self, PyObject * args )
{
    ipp_t *request = NULL;  /* IPP request object */
    ipp_t *response = NULL; /* IPP response object */
    ipp_attribute_t *attr;     /* Current IPP attribute */
    PyObject * printer_list;
    cups_lang_t * language;
    printer_list = PyList_New( 0 );

    static const char * attrs[] =         /* Requested attributes */
    {
        "printer-info",
        "printer-location",
        "printer-make-and-model",
        "printer-state",
        "printer-name",
        "device-uri",
        "printer-uri-supported",
        "printer-is-accepting-jobs",
    };

    /* Connect to the HTTP server */
    if (acquireCupsInstance() == NULL)
    {
        goto abort;
    }


    /* Assemble the IPP request */
    request = ippNew();
    language = cupsLangDefault();

    ippSetOperation( request, CUPS_GET_PRINTERS );
    ippSetRequestId ( request, 1);

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                  "attributes-charset", NULL, cupsLangEncoding( language ) );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                  "attributes-natural-language", NULL, language->language );

    ippAddStrings( request, IPP_TAG_OPERATION, IPP_TAG_KEYWORD,
                   "requested-attributes", sizeof( attrs ) / sizeof( attrs[ 0 ] ),
                   NULL, attrs );

    /* Send the request and get a response. */
    if ( ( response = cupsDoRequest( http, request, "/" ) ) == NULL )
    {
        goto abort;
    }

    Py_ssize_t max_count = 0;

    for ( attr = ippFindAttribute( response, "printer-name", IPP_TAG_NAME ),
            max_count = 0;
            attr != NULL;
            attr = ippFindNextAttribute( response, "printer-name", IPP_TAG_NAME ),
            max_count++ )
        ;

    if ( max_count > 0 )
    {
        char * device_uri = "";
        char * printer_uri = "";
        char * info = "";
        char * location = "";
        char * make_model = "";
        char * name = "";
        int accepting = 0;
        cups_ptype_t type;
        ipp_pstate_t state;
        int i = 0;

        for ( attr = ippFirstAttribute( response ); attr != NULL; attr = ippNextAttribute( response ) )
        {
            while ( attr != NULL && ippGetGroupTag( attr ) != IPP_TAG_PRINTER )
                attr = ippNextAttribute( response );

            if ( attr == NULL )
                break;

            type = CUPS_PRINTER_REMOTE;
            state = IPP_PRINTER_IDLE;
            accepting = 0;

            while ( attr != NULL && ippGetGroupTag( attr ) == IPP_TAG_PRINTER )
            {
                if ( strcmp( ippGetName( attr ), "printer-name" ) == 0 &&
                        ippGetValueTag( attr ) == IPP_TAG_NAME )
                    name = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "device-uri" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_URI )
                    device_uri = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "printer-uri-supported" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_URI )
                    printer_uri = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "printer-info" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_TEXT )
                    info = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "printer-location" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_TEXT )
                    location = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "printer-make-and-model" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_TEXT )
                    make_model = ippGetString( attr, 0, NULL );

                else if ( strcmp( ippGetName( attr ), "printer-state" ) == 0 &&
                          ippGetValueTag( attr ) == IPP_TAG_ENUM )
                    state = ( ipp_pstate_t ) ippGetInteger( attr, 0 );

                else if (!strcmp(ippGetName( attr ), "printer-is-accepting-jobs") &&
                         ippGetValueTag( attr ) == IPP_TAG_BOOLEAN)
                    accepting = ippGetBoolean( attr, 0 );

                attr = ippNextAttribute( response );
            }

            if ( device_uri == NULL )
            {
                if ( attr == NULL )
                    break;
                else
                    continue;
            }

            printer_Object * printer;
            printer = ( printer_Object * ) _newPrinter( device_uri, name, printer_uri, location, make_model,
                      info, state, accepting );

            //PyList_SetItem( printer_list, i, ( PyObject * ) printer );
            PyList_Append( printer_list, ( PyObject * ) printer );

            i++;

            if ( attr == NULL )
                break;
        }

    }
abort:
    if ( response != NULL )
        ippDelete( response );

    return printer_list;
}


PyObject * addPrinter( PyObject * self, PyObject * args )
{
    //char buf[1024];
    ipp_status_t status = IPP_BAD_REQUEST;
    ipp_t *request = NULL;  /* IPP request object */
    ipp_t *response = NULL; /* IPP response object */
    cups_lang_t * language;
    char printer_uri[ HTTP_MAX_URI ];
    char * name, * device_uri, *location, *ppd_file, * info, * model;
    const char * status_str = "successful-ok";

    if ( !PyArg_ParseTuple( args, "zzzzzz",
                            &name,             // name of printer
                            &device_uri,       // DeviceURI (e.g., hp:/usb/PSC_2200_Series?serial=0000000010)
                            &location,         // location of printer
                            &ppd_file,         // path to PPD file (uncompressed, must exist)
                            &model,            // model name (e.g., foomatic:...)
                            &info              // info/description
                          ) )
    {
        status_str = "Invalid arguments";
        goto abort;
    }

    if ( ( strlen( ppd_file ) > 0 && strlen( model ) > 0 ) ||
            ( strlen( ppd_file ) == 0 && strlen( model ) == 0) )
    {
        status_str = "Invalid arguments: specify only ppd_file or model, not both or neither";
        goto abort;
    }

    if ( !validate_name( name ) )
    {
        status_str = "Invalid printer name";
        goto abort;
    }


    sprintf( printer_uri, "ipp://localhost/printers/%s", name );

    if ( info == NULL )
        strcpy( info, name );

    cupsSetUser ("root");
    /* Connect to the HTTP server */
    if (acquireCupsInstance() == NULL)
    {
        status_str = "Unable to connect to CUPS server";
        goto abort;
    }

    /* Assemble the IPP request */
    request = ippNew();
    language = cupsLangDefault();

    ippSetOperation( request, CUPS_ADD_PRINTER );
    ippSetRequestId ( request, 1 );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                  "attributes-charset", NULL, cupsLangEncoding( language ) );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                  "attributes-natural-language", NULL, language->language );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_URI,
                  "printer-uri", NULL, printer_uri );

    ippAddInteger( request, IPP_TAG_PRINTER, IPP_TAG_ENUM,
                   "printer-state", IPP_PRINTER_IDLE );

    ippAddBoolean( request, IPP_TAG_PRINTER, "printer-is-accepting-jobs", 1 );

    ippAddString( request, IPP_TAG_PRINTER, IPP_TAG_URI, "device-uri", NULL,
                  device_uri );

    ippAddString( request, IPP_TAG_PRINTER, IPP_TAG_TEXT, "printer-info", NULL,
                  info );

    ippAddString( request, IPP_TAG_PRINTER, IPP_TAG_TEXT, "printer-location", NULL,
                  location );

    if ( strlen( model ) > 0 )
    {
        ippAddString( request, IPP_TAG_PRINTER, IPP_TAG_NAME, "ppd-name", NULL, model );

        /* Send the request and get a response. */
        response = cupsDoRequest( http, request, "/admin/" );
    }
    else
    {
        /* Send the request and get a response. */
        response = cupsDoFileRequest( http, request, "/admin/", ppd_file );
    }

    if (response == NULL)
        status = cupsLastError();
    else
        status = ippGetStatusCode( response );

    // If user cancels the authentication pop-up, changing error code to IPP_NOT_AUTHENTICATED from IPP_FORBIDDEN
    if (status == IPP_FORBIDDEN && auth_cancel_req)
    {
        status = IPP_NOT_AUTHENTICATED;
        auth_cancel_req = 0;    // Reseting cancel request.
    }

    status_str = ippErrorString( status );
    if ( status <= IPP_OK_CONFLICT )
        status =IPP_OK;

abort:
    if ( response != NULL )
        ippDelete( response );

    return Py_BuildValue( "is", status, status_str );

}

/*
 * 'delPrinter()' - Delete a printer from the system...
 */
PyObject * delPrinter( PyObject * self, PyObject * args )
{
    ipp_t * request = NULL,                        /* IPP Request */
                      *response = NULL;                /* IPP Response */
    cups_lang_t *language;                /* Default language */
    char uri[ HTTP_MAX_URI ];        /* URI for printer/class */
    char * name;
    int r = 0;
    const char *username = NULL;
    const char * status_str = "";

    username = cupsUser();

    if ( !PyArg_ParseTuple( args, "z",
                            &name ) )         // name of printer
    {
        goto abort;
    }

    if ( !validate_name( name ) )
    {
        goto abort;
    }

    cupsSetUser ("root");
    /* Connect to the HTTP server */
    if (acquireCupsInstance() == NULL)
    {
        goto abort;
    }
    snprintf( uri, sizeof( uri ), "ipp://localhost/printers/%s", name );

    /*
        * Build a CUPS_DELETE_PRINTER request, which requires the following
        * attributes:
        *
        *    attributes-charset
        *    attributes-natural-language
        *    printer-uri
       */
    request = ippNew();

    ippSetOperation( request, CUPS_DELETE_PRINTER );
    ippSetRequestId ( request, 1 );

    language = cupsLangDefault();

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                  "attributes-charset", NULL, cupsLangEncoding( language ) );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                  "attributes-natural-language", NULL, language->language );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_URI,
                  "printer-uri", NULL, uri );

    /*
     * Do the request and get back a response...
     */
    response = cupsDoRequest( http, request, "/admin/" );

    if (response == NULL)
        r = cupsLastError();
    else
        r = ippGetStatusCode( response );

    // If user cancels the authentication pop-up, changing error code to IPP_NOT_AUTHENTICATED from IPP_FORBIDDEN
    if (r == IPP_FORBIDDEN && auth_cancel_req)
    {
        r = IPP_NOT_AUTHENTICATED;
        auth_cancel_req = 0;    // Reseting cancel request.
    }

    status_str = ippErrorString( r );
    if ( r <= IPP_OK_CONFLICT )
        r = IPP_OK;

abort:
    if (username)
        cupsSetUser(username);

    if ( response != NULL )
        ippDelete( response );

    return Py_BuildValue( "is", r ,status_str);

}

/*
 * 'setDefaultPrinter()' - Set the default printing destination.
 */

PyObject * setDefaultPrinter( PyObject * self, PyObject * args )

{
    char uri[ HTTP_MAX_URI ];        /* URI for printer/class */
    ipp_t *request = NULL,                        /* IPP Request */
                     *response = NULL;                /* IPP Response */
    cups_lang_t *language;                /* Default language */
    char * name;
    int r = 0;
    const char *username = NULL;
    const char * status_str = "";

    username = cupsUser();

    if ( !PyArg_ParseTuple( args, "z",
                            &name ) )         // name of printer
    {
        goto abort;
    }

    //char buf[1024];
    //sprintf( buf, "print '%s'", name);
    //PyRun_SimpleString( buf );

    if ( !validate_name( name ) )
    {
        goto abort;
    }

    cupsSetUser ("root");
    /* Connect to the HTTP server */
    if ( acquireCupsInstance () == NULL)
    {
        goto abort;
    }

    /*
      * Build a CUPS_SET_DEFAULT request, which requires the following
      * attributes:
      *
      *    attributes-charset
      *    attributes-natural-language
      *    printer-uri
      */

    snprintf( uri, sizeof( uri ), "ipp://localhost/printers/%s", name );

    request = ippNew();

    ippSetOperation( request, CUPS_SET_DEFAULT );
    ippSetRequestId ( request, 1 );

    language = cupsLangDefault();

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                  "attributes-charset", NULL, "utf-8" ); //cupsLangEncoding( language ) );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                  "attributes-natural-language",
                  //NULL, language != NULL ? language->language : "en");
                  NULL, language->language );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_URI,
                  "printer-uri", NULL, uri );

    /*
     * Do the request and get back a response...
     */

    response = cupsDoRequest( http, request, "/admin/" );

    if (response == NULL)
        r = cupsLastError();
    else
        r = ippGetStatusCode(response );

    // If user cancels the authentication pop-up, changing error code to IPP_NOT_AUTHENTICATED from IPP_FORBIDDEN
    if (r == IPP_FORBIDDEN && auth_cancel_req)
    {
        r = IPP_NOT_AUTHENTICATED;
        auth_cancel_req = 0;    // Reseting cancel request.
    }

    status_str = ippErrorString( r );
    if ( r <= IPP_OK_CONFLICT )
        r = IPP_OK;

abort:
    if (username)
        cupsSetUser(username);

    if ( response != NULL )
        ippDelete( response );

    return Py_BuildValue( "is", r,status_str );


}



PyObject * controlPrinter( PyObject * self, PyObject * args )
{
    ipp_t *request = NULL,                 /* IPP Request */
                     *response = NULL;                /* IPP Response */
    char * name;
    int op;
    int r = IPP_BAD_REQUEST;
    char uri[ HTTP_MAX_URI ];        /* URI for printer/class */
    cups_lang_t *language;
    const char *username = NULL;
    const char * status_str = "";

    username = cupsUser();

    if ( !PyArg_ParseTuple( args, "zi", &name, &op) )
    {
        goto abort;
    }

    if ( !validate_name( name ) )
    {
        goto abort;
    }

    cupsSetUser ("root");
    /* Connect to the HTTP server */
    if (acquireCupsInstance () == NULL)
    {
        goto abort;
    }

    request = ippNew();

    ippSetOperation( request, op );
    ippSetRequestId ( request, 1 );

    language = cupsLangDefault();

    snprintf( uri, sizeof( uri ), "ipp://localhost/printers/%s", name );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                  "attributes-charset", NULL, cupsLangEncoding( language ) );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                  "attributes-natural-language", NULL, language->language );

    ippAddString( request, IPP_TAG_OPERATION, IPP_TAG_URI,
                  "printer-uri", NULL, uri );


    ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_NAME,
                 "requesting-user-name", NULL, cupsUser());

    if (op == IPP_PURGE_JOBS)
        ippAddBoolean(request, IPP_TAG_OPERATION, "purge-jobs", 1);

    response = cupsDoRequest(http, request, "/admin/");

    if (response == NULL)
        r = cupsLastError();
    else
        r = ippGetStatusCode( response );

    // If user cancels the authentication pop-up, changing error code to IPP_NOT_AUTHENTICATED from IPP_FORBIDDEN
    if (r == IPP_FORBIDDEN && auth_cancel_req)
    {
        r = IPP_NOT_AUTHENTICATED;
        auth_cancel_req = 0;    // Reseting cancel request.
    }

    status_str = ippErrorString( r );
    if ( r <= IPP_OK_CONFLICT)
        r = IPP_OK;

abort:
    if (username)
        cupsSetUser(username);

    if ( response != NULL )
        ippDelete( response );

    return Py_BuildValue( "is", r, status_str );
}



staticforward PyTypeObject job_Type;

typedef struct
{
    PyObject_HEAD
    int id;
    PyObject * dest;
    PyObject * title;
    PyObject * user;
    int state;
    int size;
}
job_Object;



static void job_dealloc( job_Object * self )
{

    Py_XDECREF( self->dest );
    Py_XDECREF( self->title );
    Py_XDECREF( self->user );
    PyObject_DEL( self );
}

static PyMemberDef job_members[] =
{
    { "id", T_INT, offsetof( job_Object, id ), 0, "Id" },
    { "dest", T_OBJECT_EX, offsetof( job_Object, dest ), 0, "Destination" },
    { "state", T_INT, offsetof( job_Object, state ), 0, "State" },
    { "title", T_OBJECT_EX, offsetof( job_Object, title ), 0, "Title" },
    { "user", T_OBJECT_EX, offsetof( job_Object, user ), 0, "User" },
    { "size", T_INT, offsetof( job_Object, size ), 0, "Size" },
    {0}
};



static PyTypeObject job_Type =
{
    PyObject_HEAD_INIT( &PyType_Type )
    0,                                     /* ob_size */
    "Job",                                 /* tp_name */
    sizeof( job_Object ),                  /* tp_basicsize */
    0,                                     /* tp_itemsize */
    ( destructor ) job_dealloc,               /* tp_dealloc */
    0,                                     /* tp_print */
    0,                                     /* tp_getattr */
    0,                                     /* tp_setattr */
    0,                                     /* tp_compare */
    0,                                     /* tp_repr */
    0,                                     /* tp_as_number */
    0,                                     /* tp_as_sequence */
    0,                                     /* tp_as_mapping */
    0,                                     /* tp_hash */
    0,                                     /* tp_call */
    0,                                     /* tp_str */
    PyObject_GenericGetAttr,               /* tp_getattro */
    PyObject_GenericSetAttr,               /* tp_setattro */
    0,                                     /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                    /* tp_flags */
    "CUPS Job object",                     /* tp_doc */
    0,                                     /* tp_traverse */
    0,                                     /* tp_clear */
    0,                                     /* tp_richcompare */
    0,                                     /* tp_weaklistoffset */
    0,                                     /* tp_iter */
    0,                                     /* tp_iternext */
    0,         /*job_methods, */                  /* tp_methods */
    job_members,                           /* tp_members */
    0,                                     /* tp_getset */
    0,                                     /* tp_base */
    0,                                     /* tp_dict */
    0,                                     /* tp_descr_get */
    0,                                     /* tp_descr_set */
    0,                                     /* tp_dictoffset */
    0,                                     /* tp_init */
    0,        //(initproc)job_init,            /* tp_init */
    0,                                     /* tp_alloc */
    //PyType_GenericAlloc,
    0,         //job_new,                       /* tp_new */
    //PyType_GenericNew,
};


static /*job_Object **/ PyObject * _newJob( int id, int state, char * dest, char * title, char * user, int size )
{
    job_Object * jo;
    jo = PyObject_New( job_Object, &job_Type );
    if ( jo == NULL )
        return NULL;
    jo->id = id;
    jo->size = size;
    jo->state = state;
    if ( dest != NULL )
        jo->dest = PyObj_from_UTF8( dest );
    else
        jo->dest = Py_BuildValue( "" );

    if ( title != NULL )
        jo->title = PyObj_from_UTF8( title );
    else
        jo->title = Py_BuildValue( "" );

    if ( user != NULL )
        jo->user = PyObj_from_UTF8( user );
    else
        jo->user = Py_BuildValue( "" );

    return ( PyObject * ) jo;

}

static /*job_Object **/ PyObject * newJob( PyObject * self, PyObject * args, PyObject * kwargs )
{
    char * dest = "";
    int id = 0;
    int state = 0;
    char * title = "";
    char * user = "";
    int size = 0;

    char * kwds[] = { "id", "state", "dest", "title", "user", "size", NULL };

    if ( !PyArg_ParseTupleAndKeywords( args, kwargs, "i|izzzi", kwds,
                                       &id, &state, &dest, &title, &user, &size ) )
        return NULL;

    return _newJob( id, state, dest, title, user, size );

}




PyObject * getDefaultPrinter( PyObject * self, PyObject * args )
{
    const char * defdest;
    defdest = cupsGetDefault();

    /*char buf[1024];
    sprintf( buf, "print 'Default Printer: %s'", defdest);
    PyRun_SimpleString( buf );
    */

    if ( defdest == NULL )
        return Py_BuildValue( "" ); // None
    else
        return Py_BuildValue( "s", defdest );

}


PyObject * cancelJob( PyObject * self, PyObject * args )         // cancelJob( dest, jobid )
{
    int status;
    int jobid;
    char * dest;

    if ( !PyArg_ParseTuple( args, "si", &dest, &jobid ) )
    {
        return Py_BuildValue( "i", 0 );
    }

    status = cupsCancelJob( dest, jobid );

    return Py_BuildValue( "i", status );
}

PyObject * getJobs( PyObject * self, PyObject * args )
{
    cups_job_t * jobs;
    Py_ssize_t i;
    int num_jobs;
    PyObject * job_list;
    int my_job;
    int completed;

    if ( !PyArg_ParseTuple( args, "ii", &my_job, &completed ) )
    {
        return PyList_New( ( Py_ssize_t ) 0 );
    }

    num_jobs = cupsGetJobs( &jobs, NULL, my_job, completed );

    if ( num_jobs > 0 )
    {
        job_list = PyList_New( num_jobs );

        for ( i = 0; i < num_jobs; i++ )
        {
            job_Object * newjob;
            newjob = ( job_Object * ) _newJob( jobs[ i ].id,
                                               jobs[ i ].state,
                                               jobs[ i ].dest,
                                               jobs[ i ].title,
                                               jobs[ i ].user,
                                               jobs[ i ].size );

            PyList_SetItem( job_list, i, ( PyObject * ) newjob );

        }
        cupsFreeJobs( num_jobs, jobs );
    }
    else
    {
        job_list = PyList_New( ( Py_ssize_t ) 0 );
    }
    return job_list;
}

PyObject * getVersion( PyObject * self, PyObject * args )
{
    return Py_BuildValue( "f", CUPS_VERSION );
}

PyObject * getVersionTuple( PyObject * self, PyObject * args )
{
    return Py_BuildValue( "(iii)", CUPS_VERSION_MAJOR, CUPS_VERSION_MINOR, CUPS_VERSION_PATCH );
}

PyObject * getServer( PyObject * self, PyObject * args )
{
    return Py_BuildValue( "s", cupsServer() );
}

PyObject * setServer( PyObject * self, PyObject * args )
{
    char * server = NULL;

    if (!PyArg_ParseTuple(args, "z", &server))
        return Py_BuildValue( "" );

    if (!strlen(server)) // Pass an empty string to restore default server
        server = NULL;

    cupsSetServer(server);

    return Py_BuildValue( "" );
}


// ***************************************************************************************************

PyObject * getPPDList( PyObject * self, PyObject * args )
{

    /*
        * Build a CUPS_GET_PPDS request, which requires the following
        * attributes:
        *
        *    attributes-charset
        *    attributes-natural-language
        *    printer-uri
        */

    ipp_t *request = NULL,                 /* IPP Request */
                     *response = NULL;                /* IPP Response */
    PyObject * result;
    cups_lang_t *language;
    ipp_attribute_t * attr;

    result = PyDict_New ();

    if (acquireCupsInstance () == NULL)
    {
        goto abort;
    }

    request = ippNew();

    ippSetOperation( request, CUPS_GET_PPDS );
    ippSetRequestId ( request, 1 );

    language = cupsLangDefault();

    ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_CHARSET,
                 "attributes-charset", NULL, cupsLangEncoding(language));

    ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_LANGUAGE,
                 "attributes-natural-language", NULL, language->language);

    //ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_URI, "printer-uri",
    //             NULL, "ipp://localhost/printers/");

    ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_URI, "printer-uri",
                 NULL, "ipp://localhost/printers/officejet_4100");

    ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_URI, "requested-attributes",
                 NULL, "all");

    /*
    * Do the request and get back a response...
    */

    if ((response = cupsDoRequest(http, request, "/")) != NULL)
    {

        for (attr = ippFirstAttribute( response ); attr; attr = ippNextAttribute( response ))
        {
            PyObject *dict;
            char *ppdname = NULL;

            while (attr && ippGetGroupTag( attr ) != IPP_TAG_PRINTER)
                attr = ippNextAttribute( response );

            if (!attr)
                break;

            dict = PyDict_New ();

            for (; attr && ippGetGroupTag( attr ) == IPP_TAG_PRINTER; attr = ippNextAttribute( response ))
            {
                PyObject *val = NULL;

                if (!strcmp (ippGetName( attr ), "ppd-name") && ippGetValueTag( attr ) == IPP_TAG_NAME)
                {
                    ppdname = ippGetString( attr, 0, NULL );

                    //sprintf( buf, "print '%s'", ppdname);
                    //PyRun_SimpleString( buf );
                }

                else if (ippGetValueTag( attr ) == IPP_TAG_TEXT || ippGetValueTag( attr ) == IPP_TAG_NAME || ippGetValueTag( attr ) == IPP_TAG_KEYWORD)
                    //else if ((!strcmp (ippGetName( attr ), "ppd-natural-language") && ippGetValueTag( attr ) == IPP_TAG_LANGUAGE) ||
                    //    (!strcmp (ippGetName( attr ), "ppd-make-and-model") && ippGetValueTag( attr ) == IPP_TAG_TEXT) ||
                    //    (!strcmp (ippGetName( attr ), "ppd-make") && ippGetValueTag( attr ) == IPP_TAG_TEXT) ||
                    //    (!strcmp (ippGetName( attr ), "ppd-device-id") && ippGetValueTag( attr ) == IPP_TAG_TEXT))
                {
                    val = PyObj_from_UTF8(ippGetString( attr, 0, NULL ));
                }

                if (val)
                {
                    PyDict_SetItemString (dict, ippGetName( attr ), val);
                    Py_DECREF (val);
                }
            }

            if (ppdname)
            {
                PyDict_SetItemString (result, ppdname, dict);
            }
            else
            {
                Py_DECREF (dict);
            }

            if (!attr)
                break;
        }

        //return result;
    }

abort:
    if ( response != NULL )
        ippDelete( response );

    return result;
}


PyObject * openPPD( PyObject * self, PyObject * args )
{
    char * printer;
    FILE * file;
    int j;

    if ( !PyArg_ParseTuple( args, "z", &printer ) )
    {
        return Py_BuildValue( "" ); // None
    }

    if ( ( g_ppd_file = cupsGetPPD( ( const char * ) printer ) ) == NULL )
    {
        goto bailout;
    }

    if ( ( file = fopen( g_ppd_file, "r" )) == NULL )
    {
        unlink(g_ppd_file);
        g_ppd_file = NULL;
        goto bailout;
    }

    ppd = ppdOpen( file );
    ppdLocalize( ppd );
    fclose( file );

    g_num_dests = cupsGetDests( &g_dests );

    if ( g_num_dests == 0 )
    {
        goto bailout;
    }

    if ( ( dest = cupsGetDest( printer, NULL, g_num_dests, g_dests ) ) == NULL )
    {
        goto bailout;
    }

    ppdMarkDefaults( ppd );
    cupsMarkOptions( ppd, dest->num_options, dest->options );

    for ( j = 0; j < dest->num_options; j++ )
    {
        if ( cupsGetOption( dest->options[ j ].name, g_num_options, g_options ) == NULL )
        {
            g_num_options = cupsAddOption( dest->options[ j ].name, dest->options[ j ].value, g_num_options, &g_options );
        }
    }

bailout:
    return Py_BuildValue( "s", g_ppd_file );
}


PyObject * closePPD( PyObject * self, PyObject * args )
{
    if ( ppd != NULL )
    {
        ppdClose( ppd );
        unlink( g_ppd_file );
    }

    ppd = NULL;

    return Py_BuildValue( "" ); // None
}


PyObject * getPPD( PyObject * self, PyObject * args )
{
    char * printer;

    if ( !PyArg_ParseTuple( args, "z", &printer ) )
    {
        return Py_BuildValue( "" ); // None
    }

    const char * ppd_file;
    ppd_file = cupsGetPPD( ( const char * ) printer );

    return Py_BuildValue( "s", ppd_file );

}


PyObject * getPPDOption( PyObject * self, PyObject * args )
{
    if ( ppd != NULL )
    {
        char * option;

        if ( !PyArg_ParseTuple( args, "z", &option ) )
        {
            return Py_BuildValue( "" ); // None
        }

        ppd_choice_t * marked_choice;
        marked_choice = ppdFindMarkedChoice( ppd, option );

        if ( marked_choice == NULL )
        {
            return Py_BuildValue( "" ); // None
        }
        else
        {
            return Py_BuildValue( "s", marked_choice->text );
        }
    }
    else
    {
        return Py_BuildValue( "" ); // None
    }
}

PyObject * findPPDAttribute( PyObject * self, PyObject * args )
{
    if ( ppd != NULL )
    {
        char * name;
        char * spec;

        if ( !PyArg_ParseTuple( args, "zz", &name, &spec ) )
        {
            return Py_BuildValue( "" ); // None
        }

        ppd_attr_t * ppd_attr;
        ppd_attr = ppdFindAttr(ppd, name, spec );
        if ( ppd_attr == NULL )
        {
            return Py_BuildValue( "" ); // None
        }
        else
        {
            return Py_BuildValue( "s", ppd_attr->value );
        }
    }
    else
    {
        return Py_BuildValue( "" ); // None
    }
}

PyObject * getPPDPageSize( PyObject * self, PyObject * args )
{
    //char buf[1024];

    if ( ppd != NULL )
    {
        ppd_size_t * size = NULL;
        float width = 0.0;
        float length = 0.0;
        ppd_choice_t * page_size = NULL;

        page_size = ppdFindMarkedChoice( ppd, "PageSize" );

        //sprintf( buf, "print '%s'", page_size->text );
        //PyRun_SimpleString( buf );

        if ( page_size == NULL )
            goto bailout;

        size = ppdPageSize( ppd, page_size->text );

        if ( size == NULL )
            goto bailout;

        //sprintf( buf, "print '%s'", size->name );
        //PyRun_SimpleString( buf );

        width = ppdPageWidth( ppd, page_size->text );
        length = ppdPageLength( ppd, page_size->text );

        return Py_BuildValue( "(sffffff)", page_size->text, width, length, size->left,
                              size->bottom, size->right, size->top );
    }

bailout:
    return Py_BuildValue( "(sffffff)", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 );
}

// ***************************************************************************************************



PyObject * resetOptions( PyObject * self, PyObject * args )
{
    if ( g_num_options > 0 )
        cupsFreeOptions( g_num_options, g_options );
    g_num_options = 0;
    g_options = ( cups_option_t * ) 0;

    return Py_BuildValue( "" );

}

PyObject * addOption( PyObject * self, PyObject * args )
{
    char * option;

    if ( !PyArg_ParseTuple( args, "z", &option ) )
    {
        return Py_BuildValue( "i", 0 );
    }

    g_num_options = cupsParseOptions( option, g_num_options, &g_options );

    return Py_BuildValue( "i", g_num_options ); // >0
}

PyObject * removeOption( PyObject * self, PyObject * args )
{
    char * option;
    int j;
    int r = 0;

    if ( !PyArg_ParseTuple( args, "z", &option ) )
    {
        return Py_BuildValue( "i", 0 );
    }

    for (j = 0; j < g_num_options; j++)
    {
        if ( !strcasecmp(g_options[j].name, option) )
        {
            g_num_options--;

            if ( j < g_num_options )
            {
                memcpy( (g_options + j), (g_options + j + 1),
                        sizeof(cups_option_t) * (g_num_options - j) );

                r = 1;
            }
        }
    }

    return Py_BuildValue( "i", r );
}


PyObject * getOptions( PyObject * self, PyObject * args )
{
    PyObject * option_list;
    int j;

    option_list = PyList_New( ( Py_ssize_t ) 0 );
    for ( j = 0; j < g_num_options; j++ )
    {
        PyList_Append( option_list, Py_BuildValue( "(ss)", g_options[ j ].name, g_options[ j ].value ) );
    }

    return option_list;
}


// ***************************************************************************************************



PyObject * getGroupList( PyObject * self, PyObject * args )
{
    PyObject * group_list;
    ppd_group_t *group;
    int i;

    /*  debug("at 0"); */

    if ( ppd != NULL && dest != NULL )
    {
        /*      debug("at 1"); */

        group_list = PyList_New( ( Py_ssize_t ) 0 );
        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            /*          debug(group->name); */
            PyList_Append( group_list, PyObj_from_UTF8( group->name ) );
        }

        return group_list;
    }

    return PyList_New( ( Py_ssize_t ) 0 );
}


PyObject * getGroup( PyObject * self, PyObject * args )
{
    const char *the_group;
    ppd_group_t *group;
    int i;

    if ( !PyArg_ParseTuple( args, "z", &the_group ) )
    {
        goto bailout;
    }

    if ( ppd != NULL && dest != NULL )
    {
        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            if ( strcasecmp( group->name, the_group ) == 0 )
            {
                return Py_BuildValue( "(si)", group->text, group->num_subgroups);
            }
        }
    }

bailout:
    return Py_BuildValue( "" );
}



PyObject * getOptionList( PyObject * self, PyObject * args )
{
    PyObject * option_list;
    const char *the_group;
    ppd_group_t *group;
    int i, j;
    ppd_option_t *option;

    if ( !PyArg_ParseTuple( args, "z", &the_group ) )
    {
        goto bailout;
    }

    if ( ppd != NULL && dest != NULL )
    {
        option_list = PyList_New( ( Py_ssize_t ) 0 );

        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            if ( strcasecmp( group->name, the_group ) == 0 )
            {
                for ( j = group->num_options, option = group->options; j > 0; j--, option++ )
                {
                    PyList_Append( option_list, PyObj_from_UTF8( option->keyword ) );
                }

                break;
            }
        }

        return option_list;
    }



bailout:
    return PyList_New( ( Py_ssize_t ) 0 );
}




PyObject * getOption( PyObject * self, PyObject * args )
{
    const char *the_group;
    const char *the_option;
    ppd_group_t *group;
    int i, j;
    ppd_option_t *option;


    if ( !PyArg_ParseTuple( args, "zz", &the_group, &the_option ) )
    {
        goto bailout;
    }

    if ( ppd != NULL && dest != NULL )
    {

        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            if ( strcasecmp( group->name, the_group ) == 0 )
            {
                for ( j = group->num_options, option = group->options; j > 0; j--, option++ )
                {
                    if ( strcasecmp( option->keyword, the_option ) == 0 )
                    {
                        return Py_BuildValue( "(ssbi)", option->text, option->defchoice,
                                              option->conflicted > 0 ? 1 : 0, option->ui );
                    }
                }
            }
        }
    }

bailout:
    return Py_BuildValue( "" );
}


PyObject * getChoiceList( PyObject * self, PyObject * args )
{
    PyObject * choice_list;
    const char *the_group;
    const char *the_option;
    ppd_group_t *group;
    int i, j, k;
    ppd_option_t *option;
    ppd_choice_t *choice;

    if ( !PyArg_ParseTuple( args, "zz", &the_group, &the_option ) )
    {
        goto bailout;
    }

    if ( ppd != NULL && dest != NULL )
    {
        choice_list = PyList_New( ( Py_ssize_t ) 0 );

        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            if ( strcasecmp( group->name, the_group ) == 0 )
            {
                for ( j = group->num_options, option = group->options; j > 0; j--, option++ )
                {
                    if ( strcasecmp( option->keyword, the_option ) == 0 )
                    {
                        for ( k = option->num_choices, choice = option->choices; k > 0; k--, choice++ )
                        {
                            PyList_Append( choice_list, PyObj_from_UTF8( choice->choice ) );
                        }

                        break;
                    }
                }
                break;
            }
        }

        return choice_list;
    }


bailout:
    return PyList_New( ( Py_ssize_t ) 0 );
}



PyObject * getChoice( PyObject * self, PyObject * args )
{
    const char * the_group;
    const char *the_option;
    const char *the_choice;
    ppd_group_t *group;
    int i, j, k;
    ppd_option_t *option;
    ppd_choice_t *choice;


    if ( !PyArg_ParseTuple( args, "zzz", &the_group, &the_option, &the_choice ) )
    {
        goto bailout;
    }

    if ( ppd != NULL && dest != NULL )
    {
        for ( i = ppd->num_groups, group = ppd->groups; i > 0; i--, group++ )
        {
            if ( strcasecmp( group->name, the_group ) == 0 )
            {
                for ( j = group->num_options, option = group->options; j > 0; j--, option++ )
                {
                    if ( strcasecmp( option->keyword, the_option ) == 0 )
                    {
                        for ( k = option->num_choices, choice = option->choices; k > 0; k--, choice++ )
                        {
                            if ( strcasecmp( choice->choice, the_choice ) == 0 )
                            {
                                return Py_BuildValue( "(sb)", choice->text, choice->marked > 0 ? 1 : 0 );
                            }
                        }
                    }
                }
            }
        }
    }


bailout:
    return Py_BuildValue( "" );



}

PyObject * setOptions( PyObject * self, PyObject * args )
{
    if ( ppd != NULL && dest != NULL )
    {
        cupsFreeOptions( dest->num_options, dest->options );
        dest->num_options = g_num_options;
        dest->options = g_options;
        cupsSetDests( g_num_dests, g_dests );
        cupsMarkOptions( ppd, dest->num_options, dest->options );
    }

    return Py_BuildValue( "" );
}

// ***************************************************************************************************

PyObject * printFileWithOptions( PyObject * self, PyObject * args )
{
    char * printer;
    char * filename;
    char * title;
    int job_id = -1;
    cups_dest_t * dests = NULL;
    cups_dest_t * dest = NULL;
    int num_dests = 0;
    int i = 0;

    if ( !PyArg_ParseTuple( args, "zzz", &printer, &filename, &title ) )
    {
        return Py_BuildValue( "" ); // None
    }

    num_dests = cupsGetDests(&dests);
    dest = cupsGetDest( printer, NULL, num_dests, dests );

    if ( dest != NULL )
    {
        for( i = 0; i < dest->num_options; i++ )
        {
            if ( cupsGetOption( dest->options[i].name, g_num_options, g_options ) == NULL )
                g_num_options = cupsAddOption( dest->options[i].name, dest->options[i].value, g_num_options, &g_options );

        }

        job_id = cupsPrintFile( dest->name, filename, title, g_num_options, g_options );

        return Py_BuildValue( "i", job_id );
    }

    return Py_BuildValue( "i", -1 );
}

// ***************************************************************************************************

static PyObject * passwordFunc = NULL;
static char *passwordPrompt = NULL;

const char * password_callback(const char * prompt)
{

    PyObject *result = NULL;
    PyObject *usernameObj = NULL;
    PyObject *passwordObj = NULL;
    char *username = NULL;
    char *password = NULL;

    if (passwordFunc != NULL)
    {

        if (passwordPrompt)
            prompt = passwordPrompt;

        result = PyObject_CallFunction(passwordFunc, "s", prompt);
        if (!result)
            return "";

        usernameObj = PyTuple_GetItem(result, 0);
        if (!usernameObj)
            return "";
        username = PyString_AsString(usernameObj);
        // printf("usernameObj=%p, username='%s'\n", usernameObj, username); 
        if (!username)
            return "";

        auth_cancel_req = ('\0' == username[0])? 1 : 0 ;

        passwordObj = PyTuple_GetItem(result, 1);
        if (!passwordObj)
            return "";
        password = PyString_AsString(passwordObj);
        // printf("passwrdObj=%p, passwrd='%s'\n", passwordObj, password); 
        if (!password)
            return "";

        cupsSetUser(username);
        return password;

    }

    return "";

}

PyObject *setPasswordPrompt(PyObject *self, PyObject *args)
{

    char *userPrompt = NULL;

    if (!PyArg_ParseTuple(args, "z", &userPrompt))
        return Py_BuildValue("");

    if (strlen(userPrompt) != 0)
        passwordPrompt = userPrompt;
    else
        passwordPrompt = NULL;

    return Py_BuildValue("");

}

PyObject * setPasswordCallback( PyObject * self, PyObject * args )
{
    if( !PyArg_ParseTuple( args, "O", &passwordFunc ) )
    {
        return Py_BuildValue( "i", 0 );
    }

    cupsSetPasswordCB(password_callback);

    return Py_BuildValue( "i", 1 );
}


PyObject * getPassword( PyObject * self, PyObject * args )
{
    const char * pwd;
    char * prompt;

    if( !PyArg_ParseTuple( args, "s", &prompt ) )
    {
        return Py_BuildValue( "" );
    }

    pwd = cupsGetPassword( prompt );

    if( pwd )
    {
        return Py_BuildValue( "s", pwd );
    }
    else
    {
        return Py_BuildValue( "" );
    }
}



// ***************************************************************************************************

static PyMethodDef cupsext_methods[] =
{
    { "getPrinters", ( PyCFunction ) getPrinters, METH_VARARGS },
    { "addPrinter", ( PyCFunction ) addPrinter, METH_VARARGS },
    { "delPrinter", ( PyCFunction ) delPrinter, METH_VARARGS },
    { "getDefaultPrinter", ( PyCFunction ) getDefaultPrinter, METH_VARARGS },
    { "setDefaultPrinter", ( PyCFunction ) setDefaultPrinter, METH_VARARGS },
    { "controlPrinter", ( PyCFunction ) controlPrinter, METH_VARARGS },
    { "getPPDList", ( PyCFunction ) getPPDList, METH_VARARGS },
    { "getPPD", ( PyCFunction ) getPPD, METH_VARARGS },
    { "openPPD", ( PyCFunction ) openPPD, METH_VARARGS },
    { "closePPD", ( PyCFunction ) closePPD, METH_VARARGS },
    { "getPPDOption", ( PyCFunction ) getPPDOption, METH_VARARGS },
    { "getPPDPageSize", ( PyCFunction ) getPPDPageSize, METH_VARARGS },
    { "getVersion", ( PyCFunction ) getVersion, METH_VARARGS },
    { "getVersionTuple", ( PyCFunction ) getVersionTuple, METH_VARARGS },
    { "cancelJob", ( PyCFunction ) cancelJob, METH_VARARGS },
    { "getJobs", ( PyCFunction ) getJobs, METH_VARARGS },
    { "getServer", ( PyCFunction ) getServer, METH_VARARGS },
    { "setServer", ( PyCFunction ) setServer, METH_VARARGS },
    { "addOption", ( PyCFunction ) addOption, METH_VARARGS },
    { "removeOption", ( PyCFunction ) removeOption, METH_VARARGS },
    { "resetOptions", ( PyCFunction ) resetOptions, METH_VARARGS },
    { "printFileWithOptions", ( PyCFunction ) printFileWithOptions, METH_VARARGS },
    { "Job", ( PyCFunction ) newJob, METH_VARARGS | METH_KEYWORDS },
    { "Printer", ( PyCFunction ) newPrinter, METH_VARARGS | METH_KEYWORDS },
    { "getGroupList", ( PyCFunction ) getGroupList, METH_VARARGS },
    { "getGroup", ( PyCFunction ) getGroup, METH_VARARGS },
    { "getOptionList", ( PyCFunction ) getOptionList, METH_VARARGS },
    { "getOption", ( PyCFunction ) getOption, METH_VARARGS },
    { "getChoiceList", ( PyCFunction ) getChoiceList, METH_VARARGS },
    { "getChoice", ( PyCFunction ) getChoice, METH_VARARGS },
    { "setOptions", ( PyCFunction ) setOptions, METH_VARARGS },
    { "getOptions", ( PyCFunction ) getOptions, METH_VARARGS },
    { "setPasswordPrompt", (PyCFunction) setPasswordPrompt, METH_VARARGS },
    { "setPasswordCallback", ( PyCFunction ) setPasswordCallback, METH_VARARGS },
    { "getPassword", ( PyCFunction ) getPassword, METH_VARARGS },
    { "findPPDAttribute", ( PyCFunction ) findPPDAttribute, METH_VARARGS },
    { "releaseCupsInstance", ( PyCFunction ) releaseCupsInstance, METH_VARARGS },
    { NULL, NULL }
};


static char cupsext_documentation[] = "Python extension for CUPS 1.x";

void initcupsext( void )
{

    PyObject * mod = Py_InitModule4( "cupsext", cupsext_methods,
                                     cupsext_documentation, ( PyObject* ) NULL,
                                     PYTHON_API_VERSION );

    if ( mod == NULL )
        return ;


}


