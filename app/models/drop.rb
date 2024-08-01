# == Schema Information
#
# Table name: drops
#
#  id         :bigint           not null, primary key
#  end_time   :datetime         not null
#  start_time :datetime         not null
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

class Drop < ApplicationRecord
  has_many :drop_items

  alias_attribute :items, :drop_items

  def floor
    items.map(&:item).pluck(:value_usd).min
  end

  def ceiling
    items.map(&:item).pluck(:value_usd).max
  end

  def total_value
    items.map(&:item).pluck(:value_usd).reduce(0.0) { |sum, el| sum + el }
  end

  def items_in_drop
    items.count
  end

  def average
    total_value / items_in_drop
  end

  def count_pulled
    items.pulled.count
  end

  def count_remaining
    items_in_drop - count_pulled
  end

  def pullable?
    items.available.any?
  end

  def pull!
    return if items.available.empty?

    item = items.available.sample

    item.update(pulled: true)

    item
  end
end
