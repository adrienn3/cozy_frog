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
require "test_helper"

class ItemTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
