# frozen_string_literal: true

class CreateDrops < ActiveRecord::Migration[7.0]
  def change
    create_table :drops do |t|
      t.datetime :start_time, null: false
      t.datetime :end_time, null: false

      t.timestamps
    end
  end
end
