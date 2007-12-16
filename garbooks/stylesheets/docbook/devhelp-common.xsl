<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
>

<!-- Customization of standard HTML stylesheet parameters -->

<xsl:param name="base.dir" select="'book/'"/>
<xsl:param name="generate.index" select="0"/>
<xsl:param name="generate.toc" select="''"/>
<xsl:param name="suppress.navigation" select="0"/>

<!-- Parameters -->

<xsl:param name="devhelp.autolabel" select="1"/>
<xsl:param name="devhelp.default.topic" select="''"/>
<xsl:param name="devhelp.encoding" select="'iso-8859-1'"/>
<xsl:param name="devhelp.chapters.section.depth" select="5"/>
<xsl:param name="devhelp.only" select="0"/>
<xsl:param name="devhelp.name" select="''"/>
<xsl:param name="devhelp.spec" select="'book.devhelp'"/>
<xsl:param name="devhelp.title" select="''"/>
<xsl:param name="devhelp.version" select="''"/>

<!-- Root -->

<xsl:template match="/">
	<xsl:call-template name="write.chunk">
		<xsl:with-param name="filename" select="$devhelp.spec"/>
		<xsl:with-param name="method" select="'xml'"/>
		<xsl:with-param name="indent" select="'yes'"/>
		<xsl:with-param name="encoding" select="$devhelp.encoding"/>
		<xsl:with-param name="content">
			<xsl:if test="$devhelp.only != 1">
				<xsl:choose>
					<xsl:when test="$rootid != ''">
						<xsl:choose>
							<xsl:when test="count(key('id',$rootid)) = 0">
								<xsl:message terminate="yes">
									<xsl:text>ID '</xsl:text>
									<xsl:value-of select="$rootid"/>
									<xsl:text>' not found in document.</xsl:text>
								</xsl:message>
							</xsl:when>
							<xsl:otherwise>
								<xsl:message>Formatting from <xsl:value-of select="$rootid"/></xsl:message>
								<xsl:apply-templates select="key('id',$rootid)" mode="process.root"/>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates select="/" mode="process.root"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:call-template name="devhelp.book"/>
		</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- Book -->

<xsl:template name="devhelp.book">
	<book>
		<xsl:if test="$devhelp.name != ''">
			<xsl:attribute name="name">
				<xsl:value-of select="$devhelp.name"/>
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="$devhelp.version != ''">
			<xsl:attribute name="version">
				<xsl:value-of select="$devhelp.version"/>
			</xsl:attribute>
		</xsl:if>
		<xsl:attribute name="title">
			<xsl:choose>
				<xsl:when test="$devhelp.title = ''">
					<xsl:choose>
						<xsl:when test="$rootid != ''">
							<xsl:apply-templates select="key('id',$rootid)" mode="title.markup"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:apply-templates select="/*" mode="title.markup"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$devhelp.title"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:choose>
				<xsl:when test="$devhelp.default.topic != ''">
					<xsl:value-of select="$devhelp.default.topic"/>
				</xsl:when>
				<xsl:otherwise>
							<xsl:choose>
								<xsl:when test="$rootid != ''">
									<xsl:apply-templates select="key('id',$rootid)" mode="chunk-filename"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:apply-templates select="/" mode="chunk-filename"/>
								</xsl:otherwise>
							</xsl:choose>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
		<xsl:call-template name="devhelp.chapters"/>
		<xsl:call-template name="devhelp.functions"/>
	</book>
</xsl:template>

<!-- Chapters -->

<xsl:template name="devhelp.chapters">
	<chapters>
		<xsl:choose>
			<xsl:when test="$rootid != ''">
				<xsl:apply-templates select="key('id',$rootid)" mode="devhelp.chapters"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="." mode="devhelp.chapters.root"/>
			</xsl:otherwise>
		</xsl:choose>
	</chapters>
</xsl:template>

<xsl:template match="set" mode="devhelp.chapters.root">
	<xsl:apply-templates select="book" mode="devhelp.chapters"/>
</xsl:template>

<xsl:template match="set" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:if test="$devhelp.autolabel=1">
			<xsl:variable name="label.markup">
				<xsl:apply-templates select="." mode="label.markup"/>
			</xsl:variable>
			<xsl:if test="normalize-space($label.markup)">
				<xsl:value-of select="concat($label.markup,$autotoc.label.separator)"/>
			</xsl:if>
		</xsl:if>
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>
	
	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:apply-templates select="book" mode="devhelp.chapters"/>
	</sub>
</xsl:template>

<xsl:template match="book" mode="devhelp.chapters.root">
	<xsl:apply-templates select="part|reference|preface|chapter|bibliography|appendix|article|colophon|glossary" mode="devhelp.chapters"/>
</xsl:template>

<xsl:template match="book" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:apply-templates select="part|reference|preface|chapter|bibliography|appendix|article|colophon|glossary" mode="devhelp.chapters"/>
	</sub>
</xsl:template>

<xsl:template match="part|reference|preface|chapter|bibliography|appendix|article|colophon|glossary" mode="devhelp.chapters.root">
	<xsl:apply-templates select="reference|preface|chapter|appendix|refentry|section|sect1|bibliodiv" mode="devhelp.chapters"/>
</xsl:template>

<xsl:template match="part|reference|preface|chapter|bibliography|appendix|article|colophon|glossary" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:apply-templates select="reference|preface|chapter|appendix|refentry|section|sect1|bibliodiv" mode="devhelp.chapters"/>
	</sub>
</xsl:template>

<xsl:template match="section" mode="devhelp.chapters.root">
	<xsl:if test="section[count(ancestor::section) &lt; $devhelp.chapters.section.depth]|refentry">
		<xsl:apply-templates select="section|refentry" mode="devhelp.chapters"/>
	</xsl:if>
</xsl:template>

<xsl:template match="section" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:if test="section[count(ancestor::section) &lt; $devhelp.chapters.section.depth]|refentry">
			<xsl:apply-templates select="section|refentry" mode="devhelp.chapters"/>
		</xsl:if>
	</sub>
</xsl:template>

<xsl:template match="sect1" mode="devhelp.chapters.root">
	<xsl:if test="sect2[$devhelp.chapters.section.depth > 1]|refentry">
		<xsl:apply-templates select="sect2|refentry" mode="devhelp.chapters"/>
	</xsl:if>
</xsl:template>

<xsl:template match="sect1" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:if test="sect2[$devhelp.chapters.section.depth > 1]|refentry">
			<xsl:apply-templates select="sect2|refentry" mode="devhelp.chapters"/>
		</xsl:if>
	</sub>
</xsl:template>

<xsl:template match="sect2" mode="devhelp.chapters.root">
	<xsl:if test="sect3[$devhelp.chapters.section.depth > 2]|refentry">
		<xsl:apply-templates select="sect3|refentry" mode="devhelp.chapters"/>
	</xsl:if>
</xsl:template>

<xsl:template match="sect2" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:if test="sect3[$devhelp.chapters.section.depth > 2]|refentry">
			<xsl:apply-templates select="sect3|refentry" mode="devhelp.chapters"/>
		</xsl:if>
	</sub>
</xsl:template>

<xsl:template match="sect3" mode="devhelp.chapters.root">
	<xsl:if test="sect4[$devhelp.chapters.section.depth > 3]|refentry">
		<xsl:apply-templates select="sect4|refentry" mode="devhelp.chapters"/>
	</xsl:if>
</xsl:template>

<xsl:template match="sect3" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:if test="sect4[$devhelp.chapters.section.depth > 3]|refentry">
			<xsl:apply-templates select="sect4|refentry" mode="devhelp.chapters"/>
		</xsl:if>
	</sub>
</xsl:template>

<xsl:template match="sect4" mode="devhelp.chapters.root">
	<xsl:if test="sect5[$devhelp.chapters.section.depth > 4]|refentry">
		<xsl:apply-templates select="sect5|refentry" mode="devhelp.chapters"/>
	</xsl:if>
</xsl:template>

<xsl:template match="sect4" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:if test="sect5[$devhelp.chapters.section.depth > 4]|refentry">
			<xsl:apply-templates select="sect5|refentry" mode="devhelp.chapters"/>
		</xsl:if>
	</sub>
</xsl:template>

<xsl:template match="sect5|refentry|colophon|bibliodiv" mode="devhelp.chapters.root">
	<xsl:apply-templates select="refentry" mode="devhelp.chapters"/>
</xsl:template>

<xsl:template match="sect5|refentry|colophon|bibliodiv" mode="devhelp.chapters">
	<xsl:variable name="title">
		<xsl:apply-templates select="." mode="title.markup.with.label.markup"/>
	</xsl:variable>

	<sub>
		<xsl:attribute name="name">
			<xsl:value-of select="normalize-space($title)"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
		<xsl:apply-templates select="refentry" mode="devhelp.chapters"/>
	</sub>
</xsl:template>

<!-- Functions -->

<!-- no separate HTML page with index -->
<xsl:template match="index"/>   
<xsl:template match="index" mode="toc"/>

<xsl:template name="devhelp.functions">
	<functions>
		<xsl:choose>
			<xsl:when test="$rootid != ''">
				<xsl:apply-templates select="key('id',$rootid)//indexterm" mode="devhelp.functions"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates select="//indexterm" mode="devhelp.functions"/>
			</xsl:otherwise>
		</xsl:choose>
	</functions>
</xsl:template>

<xsl:template match="indexterm" mode="devhelp.functions">
	<xsl:variable name="text">
		<xsl:value-of select="normalize-space(primary)"/>
		<xsl:if test="secondary">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="normalize-space(secondary)"/>
		</xsl:if>
		<xsl:if test="tertiary">
			<xsl:text>, </xsl:text>
			<xsl:value-of select="normalize-space(tertiary)"/>
		</xsl:if>
	</xsl:variable>

	<function>
		<xsl:attribute name="name">
			<xsl:value-of select="$text"/>
		</xsl:attribute>
		<xsl:attribute name="link">
			<xsl:call-template name="href.target"/>
		</xsl:attribute>
	</function>
</xsl:template>

<!-- Miscellaneous -->

<xsl:template match="*" mode="title.markup.with.label.markup">
		<xsl:if test="$devhelp.autolabel=1">
			<xsl:variable name="label.markup">
				<xsl:apply-templates select="." mode="label.markup"/>
			</xsl:variable>
			<xsl:if test="normalize-space($label.markup)">
				<xsl:value-of select="concat($label.markup,$autotoc.label.separator)"/>
			</xsl:if>
		</xsl:if>
		<xsl:apply-templates select="." mode="title.markup"/>
</xsl:template>

</xsl:stylesheet>
