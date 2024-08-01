# frozen_string_literal: true

class CreateTransactions < ActiveRecord::Migration[7.0]
  def change
    create_table :transactions do |t|
      t.references :user, null: false, foreign_key: true
      t.decimal :amount_usd, null: false, default: 0.0
      t.boolean :is_valid, null: true
      t.timestamps
    end
  end
end
