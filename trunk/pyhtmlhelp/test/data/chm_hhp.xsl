<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="text" encoding="utf-8" />

<xsl:template match="/book">[OPTIONS]
Contents file=<xsl:value-of select="@name" />.hhc
Index file=<xsl:value-of select="@name" />.hhk
Title=<xsl:value-of select="@title" />
Default topic=<xsl:value-of select="@default_link" />

[FILES]
<xsl:apply-templates select="pages" />
</xsl:template>

<xsl:template match="page">
	<xsl:value-of select="@path" />
	<xsl:text>&#10;</xsl:text>
</xsl:template>

<xsl:template match="text()" />

</xsl:stylesheet>
