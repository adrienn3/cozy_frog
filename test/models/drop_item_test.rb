# == Schema Information
#
# Table name: drop_items
#
#  id             :bigint           not null, primary key
#  pulled         :boolean          default(FALSE), not null
#  created_at     :datetime         not null
#  updated_at     :datetime         not null
#  drop_id        :bigint           not null
#  inventory_id   :bigint
#  item_id        :bigint           not null
#  transaction_id :bigint
#
# Indexes
#
#  index_drop_items_on_drop_id              (drop_id)
#  index_drop_items_on_drop_id_and_item_id  (drop_id,item_id) UNIQUE
#  index_drop_items_on_inventory_id         (inventory_id)
#  index_drop_items_on_item_id              (item_id)
#  index_drop_items_on_transaction_id       (transaction_id)
#
# Foreign Keys
#
#  fk_rails_...  (drop_id => drops.id)
#  fk_rails_...  (inventory_id => inventories.id)
#  fk_rails_...  (item_id => items.id)
#  fk_rails_...  (transaction_id => transactions.id)
#
require "test_helper"

class DropItemTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
