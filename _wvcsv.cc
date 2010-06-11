#include <Python.h>
#include "wvcsv.h"
#include "wvstring.h"
#include <vector>
#include "wvbufstream.h"
#include "wvfdstream.h"

static PyObject *pywvcsv_dequote(PyObject *self, PyObject *args)
{
    char *quoted;

    if (!PyArg_ParseTuple(args, "et", "utf-8", &quoted))
	return NULL;
    PyObject *r = Py_BuildValue("s", wvcsv_dequote(quoted, quoted));
    PyMem_Free(quoted);
    return r;
}


static PyObject *pywvcsv_quote(PyObject *self, PyObject *args)
{
    const char *unquoted;

    // Can take a 'None' type, which should be interpreted like any other.
    // 'z' allows nulls, but doesn't decode unicode properly.
    if (!PyArg_ParseTuple(args, "z", &unquoted) || unquoted)
    {
	PyErr_Clear();
	if (!PyArg_ParseTuple(args, "et", "utf-8", &unquoted))
	    return NULL;
    }
    WvString s = wvcsv_quote(unquoted);
    if (unquoted)
	PyMem_Free((void *)unquoted);
    return Py_BuildValue("s", s.cstr());
}


static PyObject *pywvcsv_splitline(PyObject *self, PyObject *args)
{
    char *line;
    std::vector<char *> v;
    std::vector<size_t> lengths;

    if (!PyArg_ParseTuple(args, "et", "utf-8", &line))
	return NULL;
    wvcsv_splitline(v, lengths, line, strlen(line), true);
    Py_ssize_t l = v.size();
    PyObject *r = PyTuple_New(l);
    for (Py_ssize_t i = 0; i < l; ++i)
	PyTuple_SET_ITEM(r, i, Py_BuildValue("s", v[i]));
    PyMem_Free(line);
    return r;
}


struct CsvContents
{
    WvStream *contents;
    WvDynBuf remainder;
    PyObject *ref;

    CsvContents(WvStream *c, PyObject *r = NULL)
    {
	contents = c;
	if (r)
	    Py_INCREF(r);
	ref = r;
    }

    ~CsvContents()
    {
	delete contents;
	if (ref)
	{
	    Py_DECREF(ref);
        }
    }
};

static PyObject *pywvcsv_setup(PyObject *self, PyObject *args)
{
    CsvContents *c;
    char *line;

    if (!PyArg_ParseTuple(args, "et", "utf-8", &line))
    {
	PyObject *f;

	PyErr_Clear();
	if (!PyArg_ParseTuple(args, "O", &f))
	    return NULL;

	if (!PyFile_Check(f))
	{
	    PyErr_SetString(PyExc_TypeError, "csvsetup needs a string/unicode "
					     "or file object");
	    return NULL;
	}

	//Handle case of file
	c = new CsvContents(new WvFdStream(dup(fileno(PyFile_AsFile(f)))), f);
    }
    else
    {
	// Case of string
	WvBufStream *s = new WvBufStream();
	s->write(line, strlen(line));  // \0
	s->seteof();
	c = new CsvContents(s);

	PyMem_Free(line);
    }

    PyObject *r = PyLong_FromLong((long)c);
    Py_INCREF(r);
    return r;
}


static PyObject *pywvcsv_takedown(PyObject *self, PyObject *args)
{
    long idx = 0;
    if (!PyArg_ParseTuple(args, "l", &idx))
	return NULL;

    CsvContents *c = (CsvContents *)idx;
    delete c;

    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *pywvcsv_readline(PyObject *self, PyObject *args)
{
    long idx = 0;
    if (!PyArg_ParseTuple(args, "l", &idx))
	return NULL;

    CsvContents *c = (CsvContents *)idx;
    char *r = wvcsv_readline(*c->contents, c->remainder);

    if (!r)
    {
	Py_INCREF(Py_None);
	return Py_None;
    }
    return Py_BuildValue("s", r);
}


static PyMethodDef wvcsv_methods[] = {
    { "dequote", pywvcsv_dequote, METH_VARARGS,
	"Dequote one CSV cell." },
    { "quote", pywvcsv_quote, METH_VARARGS,
	"Quote one CSV cell." },
    { "splitline", pywvcsv_splitline, METH_VARARGS,
	"Take one CSV-encoded line and split it, decoding each cell." },
    { "readline", pywvcsv_readline, METH_VARARGS,
	"Read one CSV-encoded line from preset buffer." },
    { "setup", pywvcsv_setup, METH_VARARGS,
	"Set up CSV reading stuff." },
    { "takedown", pywvcsv_takedown, METH_VARARGS,
	"Take down CSV reading stuff." },
    { NULL, NULL, 0, NULL },  // sentinel
};

PyMODINIT_FUNC init_wvcsv()
{
    Py_InitModule("_wvcsv", wvcsv_methods);
}
