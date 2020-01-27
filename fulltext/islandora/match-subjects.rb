require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'pry'
end

tsv_file, *files = ARGV

exit if files.empty?
exit if tsv_file.empty?
exit unless File.exist? tsv_file

# load TSV file into memory for searching
subjects = Hash.new

File.readlines(tsv_file).each do |line|
  fields = line.split("\t")
  subjects[fields[1].strip] = fields[0]
end

# iterate over files matching pattern
files.each do |filename|
  # create output file
  new_tsv = File.open("#{filename}.tsv", "w")

  # open file, iterate over subject strings
  File.readlines(filename).each do |line|
    # remove whitespance and newlines
    line.strip!
    
    # search subject string in dictionary
    if dict = subjects[line]
      # write URI, string TSV to output
      new_tsv.puts "#{dict}\t#{line}"
    else
      # if not found, mint a URN using SHA sum
      new_tsv.puts "urn:rula:#{Digest::SHA256.hexdigest(line)}\t#{line}"
    end

  end

end

exit

=begin


File.open("trimmed.ttl", "w") {|f| f << graph.dump(:turtle)}

# list of (interned) predicate URIs to strip from statements
invalid_predicates = [RDF::URI.intern('http://www.w3.org/2004/02/skos/core#changeNote'),
                      RDF::URI.intern('http://purl.org/vocab/changeset/schema#creatorName'),
                      RDF::URI.intern('http://purl.org/vocab/changeset/schema#createdDate'),
                      RDF::URI.intern('http://purl.org/vocab/changeset/schema#changeReason'),
                      RDF::URI.intern('http://purl.org/vocab/changeset/schema#subjectOfChange')]

# open the input file for reading
RDF::Reader.open("authoritiessubjects.nt.skos") do |reader|

  RDF::Writer.open("output.nt", format: :ntriples) do |writer|
      reader.each_statement do |statement|
        next if invalid_predicates.include? statement.predicate
        next if RDF::URI.intern('http://purl.org/vocab/changeset/schema#ChangeSet') == statement.object

        # write the statement to the output buffer
        writer << RDF::Repository.new do |repo|
          repo << statement
        end

        # flush the buffer to disk
        writer.flush!
      end
  end
end

=end