require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'linkeddata'
  gem 'rdf-vocab'
  gem 'pry'
end

skos_file = ARGV[0]
abort 'ERROR: Please provide a SKOS RDF file to process' if skos_file.empty?

# intern the predicates we want
pref_label = RDF::URI.intern RDF::Vocab::SKOS.prefLabel
alt_label = RDF::URI.intern RDF::Vocab::SKOS.altLabel

# open the output TSV files for writing
pref_tsv = File.open("#{skos_file}-pref.tsv", "w")
alt_tsv = File.open("#{skos_file}-alt.tsv", "w")

RDF::Reader.open(skos_file, format: :ntriples) do |reader|
  reader.each_statement do |statement|
    if statement.predicate == pref_label then
      pref_tsv.puts "<#{statement.subject}>\t#{statement.object}"

    elsif statement.predicate == alt_label then
      alt_tsv.puts "<#{statement.subject}>\t#{statement.object}"      

    end
  end
end

exit