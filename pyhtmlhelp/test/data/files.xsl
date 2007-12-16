<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="text" encoding="utf-8" />

<xsl:template match="page">
	<xsl:value-of select="@path" />
	<xsl:text>&#10;</xsl:text>
</xsl:template>

<xsl:template match="text()" />

</xsl:stylesheet>
