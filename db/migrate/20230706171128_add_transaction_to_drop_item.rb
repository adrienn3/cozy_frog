# frozen_string_literal: true

class AddTransactionToDropItem < ActiveRecord::Migration[7.0]
  def change
    add_reference :drop_items, :transaction, null: true, foreign_key: true
  end
end
