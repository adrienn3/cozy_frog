class AddInventoryIdToDropItem < ActiveRecord::Migration[7.0]
  def change
    add_reference :drop_items, :inventory, null: true, foreign_key: true
  end
end
