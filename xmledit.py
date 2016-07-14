#!/usr/bin/env python
# -*- coding: UTF-8 -*-



import cgitb
import cgi,os


from modules.logintools import login
from modules.configobj import ConfigObj
from modules.pathutils import *

print "Content-type: text/html\n\n"

editor_code="""

<!DOCTYPE html>

<title>CodeMirror: XML Autocomplete Demo</title>
<meta charset="utf-8"/>

<body>


<h1>CodeMirror Tryout</h1>
<p>email:<i>zangsir@gmail.com</i></p>
<p>features: no indentation; autocomplete<p>
<div>



<link rel="stylesheet" href="codemirror-5.15.2/lib/codemirror.css">
<link rel="stylesheet" href="codemirror-5.15.2/addon/hint/show-hint.css">
<script src="codemirror-5.15.2/lib/codemirror.js"></script>
<script src="codemirror-5.15.2/addon/hint/show-hint.js"></script>
<script src="codemirror-5.15.2/addon/hint/xml-hint.js"></script>
<script src="codemirror-5.15.2/mode/xml/xml.js"></script>
<style type="text/css">
      .CodeMirror { border: 1px solid #eee; }
    </style>


<article>

<form><textarea id="code" name="code"><!-- write some xml below -->
</textarea></form>

    <script>
      var dummy = {
        attrs: {
          color: ["red", "green", "blue", "purple", "white", "black", "yellow"],
          size: ["large", "medium", "small"],
          description: null
        },
        children: []
      };

      var tags = {
        "!top": ["top"],
        "!attrs": {
          id: null,
          class: ["A", "B", "C"]
        },
        top: {
          attrs: {
            lang: ["en", "de", "fr", "nl"],
            freeform: null
          },
          children: ["animal", "plant"]
        },
        animal: {
          attrs: {
            name: null,
            isduck: ["yes", "no"]
          },
          children: ["wings", "feet", "body", "head", "tail"]
        },
        plant: {
          attrs: {name: null},
          children: ["leaves", "stem", "flowers"]
        },
        wings: dummy, feet: dummy, body: dummy, head: dummy, tail: dummy,
        leaves: dummy, stem: dummy, flowers: dummy
      };

      function completeAfter(cm, pred) {
        var cur = cm.getCursor();
        if (!pred || pred()) setTimeout(function() {
          if (!cm.state.completionActive)
            cm.showHint({completeSingle: false});
        }, 100);
        return CodeMirror.Pass;
      }

      function completeIfAfterLt(cm) {
        return completeAfter(cm, function() {
          var cur = cm.getCursor();
          return cm.getRange(CodeMirror.Pos(cur.line, cur.ch - 1), cur) == "<";
        });
      }

      function completeIfInTag(cm) {
        return completeAfter(cm, function() {
          var tok = cm.getTokenAt(cm.getCursor());
          if (tok.type == "string" && (!/['"]/.test(tok.string.charAt(tok.string.length - 1)) || tok.string.length == 1)) return false;
          var inner = CodeMirror.innerMode(cm.getMode(), tok.state).state;
          return inner.tagName;
        });
      }

      var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: "xml",
        lineNumbers: true,indentUnit:0,
        extraKeys: {
          "'<'": completeAfter,
          "'/'": completeIfAfterLt,
          "' '": completeIfInTag,
          "'='": completeIfInTag,
          "Ctrl-Space": "autocomplete"
        },
        hintOptions: {schemaInfo: tags}
      });
    </script>




</article>
</div>
</body>"""



def open_main_server():
	thisscript = os.environ.get('SCRIPT_NAME', '')
	action = None
	theform = cgi.FieldStorage()
	scriptpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
	userdir = scriptpath + "users" + os.sep
	action, userconfig = login(theform, userdir, thisscript, action)
	print editor_code


open_main_server()
