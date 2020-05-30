#  rdf2tsv.rb
#
#  Given a SKOS vocabulary in RDF format (eg. LCSH),
#  generate 2 TSV files of term/URI pairs:
#  one for prefLabels, one for altLabels
#

require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'linkeddata'
  gem 'rdf-vocab'
end

skos_file = ARGV[0]
abort 'ERROR: Please provide a SKOS RDF file to process' if skos_file.nil? || skos_file.empty?

# intern the predicates we want
pref_label = RDF::URI.intern RDF::Vocab::SKOS.prefLabel
alt_label = RDF::URI.intern RDF::Vocab::SKOS.altLabel

# open the output TSV files for writing
pref_tsv = File.open("#{skos_file}-pref.tsv", "w")
alt_tsv = File.open("#{skos_file}-alt.tsv", "w")

RDF::Reader.open(skos_file) do |reader|
  reader.each_statement do |statement|
    tsv_line = "<#{statement.subject}>\t#{statement.object}"

    if statement.predicate == pref_label then pref_tsv.puts tsv_line
    elsif statement.predicate == alt_label then alt_tsv.puts tsv_line
    end
  end
end

exit