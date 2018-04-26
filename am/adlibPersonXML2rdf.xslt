<?xml version="1.0" encoding="UTF-8"?>
<!-- adlibPersonXML2rdf voor Amsterdam Museum data -->
<!-- CC0 Ivo Zandhuis (https://ivozandhuis.nl) -->
<!-- 20180326 -->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:edm="http://www.europeana.eu/schemas/edm/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/"
  xmlns:sem="http://semanticweb.cs.vu.nl/2009/11/sem/"
  xmlns:schema="http://schema.org/"
  xmlns:void="http://rdfs.org/ns/void#"
  xmlns:owl="http://www.w3.org/2002/07/owl#"
  >

  <xsl:output method="xml" indent="yes"/>

  <xsl:variable name="collect">
    <xsl:text>http://hdl.handle.net/11259/people.</xsl:text>
  </xsl:variable>

  <!-- basic structure -->
  <xsl:template match="/">
    <xsl:apply-templates select="adlibXML"/>
  </xsl:template>

  <xsl:template match="adlibXML">
    <xsl:apply-templates select="recordList"/>
  </xsl:template>

  <xsl:template match="recordList">
    <xsl:element name="rdf:RDF">
      <xsl:apply-templates select="record"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="record">
    <xsl:element name="rdf:Description">
      <xsl:attribute name="rdf:about">
        <xsl:value-of select="concat($collect, priref)"/>
      </xsl:attribute>
      <!--void:inDataset rdf:resource="https://data.adamlink.nl/am/amperson/"></void:inDataset-->
      <xsl:apply-templates select="name"/>
      <xsl:apply-templates select="name.type"/>
      <xsl:apply-templates select="link_url"/>
      <xsl:apply-templates select="birth.date.start"/>
      <xsl:apply-templates select="birth.place"/>
      <xsl:apply-templates select="death.date.start"/>
      <xsl:apply-templates select="death.place"/>
      <xsl:apply-templates select="occupation"/>
    </xsl:element>
  </xsl:template>

  <!-- matching elements -->
  <xsl:template match="name">
    <xsl:element name="foaf:name">
      <xsl:value-of select="."/>
    </xsl:element>
    <xsl:element name="rdfs:label">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="name.type">
    <xsl:choose>
      <xsl:when test="(value[@lang='neutral'] = 'AUTHOR') or (value[@lang='neutral'] = 'PERSON')">
        <xsl:element name="rdf:type">
          <xsl:attribute name="rdf:resource">
            <xsl:text>http://schema.org/Person</xsl:text>
          </xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:when test="value[@lang='neutral'] = 'CORPORATE' or value[@lang='neutral'] = 'INST'">
        <xsl:element name="rdf:type">
          <xsl:attribute name="rdf:resource">
            <xsl:text>http://schema.org/Organization</xsl:text>
          </xsl:attribute>
        </xsl:element>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="link_url">
    <xsl:element name="owl:sameAs">
      <xsl:attribute name="rdf:resource">
        <xsl:value-of select="normalize-space(.)"/>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="birth.date.start">
    <xsl:element name="schema:birthDate">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="birth.place">
    <xsl:element name="schema:birthPlace">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="death.date.start">
    <xsl:element name="schema:deathDate">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="death.place">
    <xsl:element name="schema:deathPlace">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="occupation">
    <xsl:element name="schema:jobTitle">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
