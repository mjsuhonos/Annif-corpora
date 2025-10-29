<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:marc="http://www.loc.gov/MARC21/slim"
	exclude-result-prefixes="marc">

    <xsl:output method="text" omit-xml-declaration="yes" indent="no" media-type="string"/>

    <!-- Match the root element and apply templates for each record -->
    <xsl:template match="/marc:collection">
        <xsl:apply-templates select="marc:record"/>
    </xsl:template>

    <!-- Match each record element -->
    <xsl:template match="marc:record">
        <!-- Find and process the 001 datafield -->
        <xsl:apply-templates select="marc:controlfield[@tag='001']"/>
        <xsl:text>&#x9;</xsl:text> <!-- tab character -->
        <!-- Find and process the 245 datafield -->
        <xsl:apply-templates select="marc:datafield[@tag='245' or @tag='246']"/>
        <!-- Find and process the 650 datafield -->
        <xsl:apply-templates select="marc:datafield[@tag='650']"/>
        <!-- Add a newline at the end of each record -->
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

    <!-- Template to process datafield tag="001" -->
    <xsl:template match="marc:controlfield[@tag='001']">
        <xsl:value-of select="."/>
    </xsl:template>

    <!-- Template to process datafield tag="245" -->
    <xsl:template match="marc:datafield[@tag='245' or @tag='246']">
        <xsl:value-of select="translate(marc:subfield[@code='a'], '/&quot;', '')"/><xsl:text> </xsl:text>
        <xsl:value-of select="translate(marc:subfield[@code='b'], '/&quot;', '')"/>
    </xsl:template>

    <!-- Template to process datafield tag="650" -->
    <xsl:template match="marc:datafield[@tag='650']">
        <xsl:text>&#x9;</xsl:text> <!-- tab character -->
        <xsl:for-each select="marc:subfield">
            <!-- Concatenate subfields with a dash if not the first subfield -->
            <xsl:if test="position() != 1">
                <xsl:text>--</xsl:text>
            </xsl:if>
            <xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>