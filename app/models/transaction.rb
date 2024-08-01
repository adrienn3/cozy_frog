# == Schema Information
#
# Table name: transactions
#
#  id           :bigint           not null, primary key
#  amount_usd   :decimal(10, )    default(0), not null
#  is_valid     :boolean
#  created_at   :datetime         not null
#  updated_at   :datetime         not null
#  drop_item_id :bigint
#  user_id      :bigint           not null
#
# Indexes
#
#  index_transactions_on_drop_item_id  (drop_item_id)
#  index_transactions_on_user_id       (user_id)
#
# Foreign Keys
#
#  fk_rails_...  (drop_item_id => drop_items.id)
#  fk_rails_...  (user_id => users.id)
#
class Transaction < ApplicationRecord
  before_create :check_account_balance

  has_one :drop_item

  def check_account_balance
    user = User.find(user_id) # Assuming `user_id` is an attribute of the model
    self.is_valid = user.account_balance.positive?
  end
end
