<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">

<xsl:output method="html" encoding="UTF-8" doctype-system="about:legacy-compat" indent="yes"/>

<xsl:template match="/tei:TEI">
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></title>
<style>
  body{font-family:Georgia,'Times New Roman',serif;max-width:900px;margin:2rem auto;padding:0 1.5rem;line-height:1.65;color:#2b2620;background:#fbf9f5;}
  h1{font-size:1.9rem;border-bottom:3px solid #8a5a2b;padding-bottom:.4rem;}
  h2{color:#8a5a2b;margin-top:2.5rem;}
  .text p{font-size:1.06rem;}
  .entity{border-bottom:2px dotted #8a5a2b;text-decoration:none;color:#5a3d1a;font-weight:600;}
  .entity:hover{background:#f1e3cf;}
  table{border-collapse:collapse;width:100%;margin-top:.8rem;font-size:.9rem;}
  th,td{border:1px solid #d8cdb8;padding:.5rem .7rem;text-align:left;vertical-align:top;}
  th{background:#efe4d1;}
  caption{caption-side:top;font-weight:bold;margin-bottom:.4rem;text-align:left;color:#8a5a2b;}
  .source{font-size:.85rem;color:#6b6255;margin-top:2.5rem;border-top:1px solid #d8cdb8;padding-top:.8rem;}
</style>
</head>
<body>
<h1><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h1>

<div class="text">
<xsl:apply-templates select="tei:text/tei:body/tei:div/tei:p"/>
</div>

<h2>Persons</h2>
<table>
<caption>Entities of type Person</caption>
<tr><th>Name</th><th>Description</th><th>Wikidata</th><th>Wikipedia</th></tr>
<xsl:for-each select="tei:standOff/tei:listPerson/tei:person">
<tr>
<td><xsl:value-of select="tei:persName"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
<td><a href="{tei:idno[@type='wikipedia']}">link</a></td>
</tr>
</xsl:for-each>
</table>

<h2>Places</h2>
<table>
<caption>Entities of type Place</caption>
<tr><th>Name</th><th>Description</th><th>Wikidata</th><th>Wikipedia</th></tr>
<xsl:for-each select="tei:standOff/tei:listPlace/tei:place">
<tr>
<td><xsl:value-of select="tei:placeName"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
<td><a href="{tei:idno[@type='wikipedia']}">link</a></td>
</tr>
</xsl:for-each>
</table>

<h2>Organizations</h2>
<table>
<caption>Entities of type Organization</caption>
<tr><th>Name</th><th>Description</th><th>Wikidata</th><th>Wikipedia</th></tr>
<xsl:for-each select="tei:standOff/tei:listOrg/tei:org">
<tr>
<td><xsl:value-of select="tei:orgName"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
<td><a href="{tei:idno[@type='wikipedia']}">link</a></td>
</tr>
</xsl:for-each>
</table>

<h2>Monuments / Buildings</h2>
<table>
<caption>Entities of type Monument (with sub-type)</caption>
<tr><th>Name</th><th>Sub-type</th><th>Description</th><th>Wikidata</th><th>Wikipedia</th></tr>
<xsl:for-each select="tei:standOff/tei:list[@type='monuments']/tei:item">
<tr>
<td><xsl:value-of select="tei:name"/></td>
<td><xsl:value-of select="@type"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
<td><a href="{tei:idno[@type='wikipedia']}">link</a></td>
</tr>
</xsl:for-each>
</table>

<h2>Concepts (Religion / Language)</h2>
<table>
<caption>Entities of type Concept</caption>
<tr><th>Name</th><th>Description</th><th>Wikidata</th><th>Wikipedia</th></tr>
<xsl:for-each select="tei:standOff/tei:list[@type='concepts']/tei:item">
<tr>
<td><xsl:value-of select="tei:name"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
<td><a href="{tei:idno[@type='wikipedia']}">link</a></td>
</tr>
</xsl:for-each>
</table>

<h2>Document Archive</h2>
<table>
<caption>Bibliographic / archival entity</caption>
<tr><th>Title</th><th>Description</th><th>Wikidata</th></tr>
<xsl:for-each select="tei:standOff/tei:listBibl/tei:bibl[tei:title]">
<tr>
<td><xsl:value-of select="tei:title[1]"/></td>
<td><xsl:value-of select="tei:desc"/></td>
<td><a href="{tei:idno[@type='wikidata']}"><xsl:value-of select="tei:idno[@type='wikidata']"/></a></td>
</tr>
</xsl:for-each>
</table>

<h2>Relations (30 total)</h2>
<table>
<caption>Relations between entities (theoretical/conceptual model)</caption>
<tr><th>Subject</th><th>Predicate</th><th>Object</th></tr>
<xsl:for-each select="tei:standOff/tei:listRelation/tei:relation">
<tr>
<td><xsl:value-of select="translate(@active,'#','')"/></td>
<td><xsl:value-of select="@name"/></td>
<td><xsl:value-of select="translate(@passive,'#','')"/></td>
</tr>
</xsl:for-each>
</table>

<p class="source">
Source: adapted from <a href="{tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:ref/@target}">Wikipedia - Persepolis</a>.
Encoded in TEI/XML and transformed to HTML with XSLT for a university course project
(Information Science and Cultural Heritage, a.y. 2025-2026, DHDK, University of Bologna).
</p>

</body>
</html>
</xsl:template>

<!-- inline entity mentions become highlighted links -->
<xsl:template match="tei:placeName|tei:persName|tei:orgName|tei:name">
  <xsl:variable name="id" select="translate(@ref,'#','')"/>
  <a class="entity">
    <xsl:attribute name="href">#<xsl:value-of select="$id"/></xsl:attribute>
    <xsl:apply-templates/>
  </a>
</xsl:template>

<xsl:template match="tei:ref[@type='citation']">
  <sup>[src]</sup>
</xsl:template>

</xsl:stylesheet>
