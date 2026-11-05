# Implementation provenance

This personal skill and helper were authored for this installation. The helper is
an original implementation using Python `zipfile` and `lxml`; it does not copy the
managed Documents plugin's helper, license, or other files. The regression tests
were authored during the local investigation and exercise consumer-visible DOCX
behavior independently of the implementation.

The investigation identified that unwrapping a rejected deletion while retaining
`w:delText` loses normal paragraph text. WordprocessingML distinguishes
[deleted text](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.deletedtext?view=openxml-3.0.1)
from ordinary text; this helper restores ordinary text when retaining deleted content.

The managed Documents plugin remains unchanged. Its `LICENSE.txt` applies OpenAI
service terms and additional restrictions; it is not an MIT license. The separate
staged repair remains local review evidence and is not the deployed implementation.
