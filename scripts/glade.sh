#!/bin/sh

# Helper script to run the Glade UI designer

# rootdir=`dirname $0`

rootdir=`pwd`
echo "directory = $rootdir"
if [ ! -f "$rootdir/README.rst" ] ; then
  echo "This script must be run in the Sage Desktop project root directory"
  echo "That is, the directory containing README.rst"
fi

CATALOG_DTD=/usr/share/glade3/catalogs/glade-catalog.dtd
if [ -f "$CATALOG_DTD" ] ; then
    xmllint --dtdvalid "$CATALOG_DTD" --noout src/sageui/view/glade/sourceview.xml
    xmllint --dtdvalid "$CATALOG_DTD" --noout src/sageui/view/glade/sageui.xml
fi

export GLADE_CATALOG_PATH=$rootdir/src/sageui/view/glade
export GLADE_MODULE_SEARCH_PATH=$rootdir/src/sageui/view/glade

echo "GLADE_CATALOG_PATH=$GLADE_CATALOG_PATH"
echo "GLADE_MODULE_SEARCH_PATH=$GLADE_MODULE_SEARCH_PATH"

glade -v src/sageui/res/SageUI.xml
