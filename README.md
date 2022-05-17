# labelstudio-to-fonduer

This small module connects Label Studio with Fondue by creating a fonduer labeling function for gold labels from a Label Studio export.

Gold labeled candidates are identified by matching:
`document id` (identified by filename)
string
 `sentence id`
the character offset in the sentence

## Installation:
To install, simply run: 
```
pip install git+https://github.com/jueri/labelstudio-to-fonduer.git#egg=labelstudiotofonduer\&subdirectory=src
```

## Usage:
The example notebook provides a full fonduer pipeline and shows how the module can be used to import the labels from the example Label Studio export.

Most important, an export can be parsed in conjunction with the label studio session

```Python
from LabelstudioToFonduer.ls_export import Export

export = Export(session, "export_1.json")
```
to create the `gold` labeling function
```Python
gold = export.is_gold
```

