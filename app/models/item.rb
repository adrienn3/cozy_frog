# frozen_string_literal: true

# == Schema Information
#
# Table name: items
#
#  id                :bigint           not null, primary key
#  name              :string(255)      default("item_placeholder"), not null
#  release_year      :integer
#  unique_identifier :string(255)
#  value_usd         :decimal(10, )    default(0), not null
#  created_at        :datetime         not null
#  updated_at        :datetime         not null
#

class Item < ApplicationRecord
    has_one_attached :image
end
