<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="html" encoding="iso-8859-1" indent="yes" />

	<xsl:template match="contents">
		<ul>
			<xsl:apply-templates />
		</ul>
	</xsl:template>

	<xsl:template match="contents_entry">
		<li>
			<object type="text/sitemap">
				<param name="Name" value="{@name}" />
				<param name="Local" value="{@link}" />
			</object>
			<xsl:if test="contents_entry">
				<ul>
					<xsl:apply-templates />
				</ul>
			</xsl:if>
		</li>
	</xsl:template>

	<xsl:template match="text()" />

</xsl:stylesheet>
