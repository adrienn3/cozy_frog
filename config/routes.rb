# frozen_string_literal: true

Rails.application.routes.draw do
  devise_for :users

  devise_scope :user do
    get '/users/sign_out' => 'devise/sessions#destroy'
  end

  get root to: 'application#hello'
  get 'pull', to: 'application#pull'
  get 'pull_item', to: 'application#pull_item'
  get 'purchase_item', to: 'application#purchase_item'
  get 'about', to: 'application#about'
  get 'account', to: 'application#account'
  get 'inventory', to: 'application#inventory'
  get 'disenchant', to: 'application#disenchant'
end
