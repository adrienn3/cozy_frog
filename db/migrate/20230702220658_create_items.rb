# frozen_string_literal: true

class CreateItems < ActiveRecord::Migration[7.0]
  def change
    create_table :items do |t|
      t.string :name, null: false, default: 'item_placeholder'
      t.decimal :value_usd, null: false, default: 0.0

      t.string :unique_identifier, null: true
      t.integer :release_year, null: true

      t.timestamps
    end
  end
end
