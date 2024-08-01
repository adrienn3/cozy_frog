# frozen_string_literal: true

class CreateDropItems < ActiveRecord::Migration[7.0]
  def change
    create_table :drop_items do |t|
      t.references :drop, null: false, foreign_key: true
      t.references :item, null: false, foreign_key: true

      t.timestamps
    end

    add_index :drop_items, %i[drop_id item_id], unique: true
  end
end
