<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.devhelp.net/book" version="1.0">

<xsl:output method="text" encoding="utf-8"/>

<xsl:template match="/book"><!--
--># Generated automatically - do not modify
	
from htmlhelp.book import *
from htmlhelp.archive.dir import DirArchive

<xsl:apply-templates />
archive = DirArchive("""data/<xsl:value-of select="@name"/>""")

book = Book(name="""<xsl:value-of select="@name"/>""", archive=archive, contents=contents, index=index)
</xsl:template>

<xsl:template match="contents">
contents = ContentsEntry("""<xsl:value-of select="/book/@title"/>""", """<xsl:value-of select="/book/@default_link"/>""")
_parent = contents
<xsl:apply-templates />
</xsl:template>

<xsl:template match="contents_entry"><!--
-->_entry = ContentsEntry("""<xsl:value-of select="@name"/>""", """<xsl:value-of select="@link"/>""")
_parent.append(_entry)
<xsl:if test="contents_entry"><!--
-->_parent = _entry
<xsl:apply-templates /><!--
-->_parent = _parent.parent
</xsl:if>
</xsl:template>

<xsl:template match="index">
index = Index()
<xsl:apply-templates />
</xsl:template>

<xsl:template match="index_entry"><!--
-->index.append(IndexEntry("""<xsl:value-of select="@name"/>""", """<xsl:value-of select="@link"/>"""))
</xsl:template>

<xsl:template match="text()" />

</xsl:stylesheet>
