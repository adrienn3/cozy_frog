class AddAccountBalanceToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :account_balance, :decimal, precision: 10, scale: 2, default: 0, null: false
  end
end
