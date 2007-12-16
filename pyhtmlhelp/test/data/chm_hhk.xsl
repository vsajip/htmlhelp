<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html" encoding="iso-8859-1" indent="yes" />

	<xsl:template match="index">
		<ul>
			<xsl:apply-templates />
		</ul>
	</xsl:template>

	<xsl:template match="index_entry">
		<li>
			<object type="text/sitemap">
				<param name="Name" value="{@name}" />
				<param name="Local" value="{@link}" />
			</object>
		</li>
	</xsl:template>

	<xsl:template match="text()" />

</xsl:stylesheet>
