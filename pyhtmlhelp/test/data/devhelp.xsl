<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.devhelp.net/book" version="1.0">

	<xsl:output method="xml" encoding="utf-8" indent="yes" />

	<xsl:template match="/book">
		<book name="{@name}" title="{@title}" link="{@default_link}" author="">
			<xsl:apply-templates />
		</book>
	</xsl:template>

	<xsl:template match="contents">
		<chapters>
			<xsl:apply-templates />
		</chapters>
	</xsl:template>

	<xsl:template match="contents_entry">
		<sub name="{@name}" link="{@link}">
			<xsl:apply-templates />
		</sub>
	</xsl:template>

	<xsl:template match="index">
		<functions>
			<xsl:apply-templates />
		</functions>
	</xsl:template>

	<xsl:template match="index_entry">
		<function name="{@name}" link="{@link}" />
	</xsl:template>

	<xsl:template match="text()" />

</xsl:stylesheet>
