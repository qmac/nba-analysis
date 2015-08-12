require 'csv'
require 'json'
SIZE = 2000

players = []
result = {}
CSV.foreach('results.csv') do |row|
  players << {
    :name => row[1],
    :tier => row[2].to_i
  }
end

players_grouped = players.group_by { |p| p[:tier] }

result[:name] = 'vis'
result[:children] = players_grouped.map do |tier, player_array|
  {
    :name => "Tier #{tier}",
    :children => player_array.map { |p| {:name => p[:name], :size => SIZE} }
  }
end

open('nba.json', 'w') { |f|
  f.puts result.to_json
}