# frozen_string_literal: true

class AddItemToTransaction < ActiveRecord::Migration[7.0]
  def change
    add_reference :transactions, :drop_item, null: true, foreign_key: true
  end
end
