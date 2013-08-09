#!/bin/sh

# Helper script to run the Glade UI designer

# rootdir=`dirname $0`

rootdir=`pwd`
echo "directory = $rootdir"
if [ ! -x "$rootdir/README.rst" ] ; then
  echo "This script must be run in the Sage Desktop project root directory"
  echo "That is, the directory containing README.rst"
fi


export GLADE_CATALOG_PATH=$rootdir/src/sageui/view/glade
export GLADE_MODULE_PATH=$rootdir/src/sageui/view/glade

echo $GLADE_CATALOG_PATH
echo $GLADE_MODULE_PATH

glade-3 -v src/sageui/res/SageUI.xml
