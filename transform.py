"""
transform.py
Applies style.xsl to data.xml (TEI) and writes the resulting HTML page.
Course project: Information Science and Cultural Heritage, a.y. 2025-2026, DHDK.
Requires: lxml (pip install lxml --break-system-packages)
"""
from lxml import etree

xml_doc = etree.parse("data.xml")
xslt_doc = etree.parse("style.xsl")
transform = etree.XSLT(xslt_doc)
result = transform(xml_doc)

with open("output.html", "wb") as f:
    f.write(etree.tostring(result, pretty_print=True, method="html", encoding="utf-8"))

print("Wrote output.html")
