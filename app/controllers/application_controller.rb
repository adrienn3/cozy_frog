# frozen_string_literal: true

class ApplicationController < ActionController::Base
  before_action :load_drop, only: %i[pull_item]
  # before_action :authenticate_user!, only: %i[pull_item]

  def hello
    @drop = Drop.last&.decorate

    render layout: 'layouts/application'
  end

  def about; end

  def pull; end

  def account; end

  def inventory; end

  def disenchant; end

  def pull_item
    balance = current_user.account_balance
    current_user.update!(account_balance: balance - 1)
    render json: { pulled: '1x booster box' }
    # @drop = Drop.create!
    # if @drop&.pullable?
    #   txn = Transaction.create!(user_id: current_user.id, amount_usd: 10.00)

    #   if txn.is_valid
    #     current_user.update!(account_balance: current_user.account_balance - 10)
    #     @item = @drop&.pull!
    #     @item.update!(inventory_id: current_user.inventory.id)
    #     txn.update!(drop_item: @item)
    #     @item = @item.item
    #     render
    #   else
    #     render json: { error: 'INSUFFICIENT_FUNDS' }, status: :unprocessable_entity
    #   end

    # else
    #   @error = 'UNAVAILABLE'
    #   render
    # end
  end

  def purchase_item
    item = Item.find_or_create_by(name: 'OP-01')
    drop = Drop.create!(start_time: Time.current, end_time: Time.current)
    DropItem.create!(item:, drop:)
    render
  end

  private

  def load_drop
    @drop = Drop.last
  end
end
