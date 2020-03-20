require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'linkeddata'
  gem 'rdf-vocab'
  gem 'pry'
end

tsv_file = ARGV[0]
abort 'ERROR: Please provide a TSV file to process' if tsv_file.nil? || tsv_file.empty?

# intern the predicates we want
pref_label = RDF::URI.intern RDF::Vocab::SKOS.prefLabel
alt_label = RDF::URI.intern RDF::Vocab::SKOS.altLabel

# open the output file for writing
RDF::Writer.open("#{tsv_file}.nt") do |writer|

  # open file, iterate over subject strings
  File.readlines(tsv_file).each do |line|
    fields = line.split("\t")
    subject = RDF::URI(fields[0].gsub(/[\<\>]/, ''))

    writer << RDF::Statement.new(subject, RDF::Vocab::SKOS.prefLabel, RDF::Literal.new(fields[1].chomp, language: :en))
    writer << RDF::Statement.new(subject, RDF.type, RDF::Vocab::SKOS.Concept)
  end

end

exit