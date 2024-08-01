# frozen_string_literal: true

class AddPulledToDropItems < ActiveRecord::Migration[7.0]
  def change
    add_column :drop_items, :pulled, :boolean, null: false, default: false
  end
end
