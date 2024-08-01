# frozen_string_literal: true

class DropDecorator < Draper::Decorator
  delegate_all

  def pulled_to_string
    "#{count_remaining}/#{items.count}"
  end

  def total_to_string_usd
    "$#{format('%.0f', total_value)}"
  end

  def floor_to_string_usd
    "$#{format('%.0f', floor)}"
  end

  def ceiling_to_string_usd
    "$#{format('%.0f', ceiling)}"
  end

  def average_to_string_usd
    "$#{format('%.0f', average)}"
  end
end
