#pragma once

#include "ringbuf.hpp"

enum class EKeyEvent {
  None = 0x00,
  Released = 0x01,
  Pressed = 0x02,
};

using keycode_t = uint16_t;

struct KeyEvent {
  KeyEvent(keycode_t _code = 0, EKeyEvent _event = EKeyEvent::None, int16_t _tick_ms = 0)
      : code(_code), event(_event), tick_ms(_tick_ms) {}
  keycode_t code;
  EKeyEvent event;
  int16_t tick_ms;

  inline bool isPressed() const { return event == EKeyEvent::Pressed; }
};

using KeyEventBuffer = RingBuffer<KeyEvent>;
