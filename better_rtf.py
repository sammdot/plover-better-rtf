from plover.steno import STROKE_DELIMITER
from plover.steno_dictionary import StenoDictionary
import rtfcre

class RtfDictionary(StenoDictionary):
  def __init__(self):
    self._rtf_dict = rtfcre.RtfDictionary()
    StenoDictionary.__init__(self)

  def _load(self, filename):
    with open(filename, "rb") as file:
      self._rtf_dict = rtfcre.load(file)

  def _save(self, filename):
    with open(filename, "wb") as file:
      self._rtf_dict.dump(file)

  def __len__(self):
    return len(self._rtf_dict)

  def __contains__(self, steno):
    return STROKE_DELIMITER.join(steno) in self._rtf_dict

  def __getitem__(self, steno):
    return self._rtf_dict[STROKE_DELIMITER.join(steno)]

  def get(self, steno, default=None):
    try:
      return self[steno]
    except KeyError:
      return default

  def __setitem__(self, steno, translation):
    self._rtf_dict[STROKE_DELIMITER.join(steno)] = translation

  def __delitem__(self, steno):
    del self._rtf_dict[STROKE_DELIMITER.join(steno)]

  @property
  def _longest_key(self):
    return self._rtf_dict.longest_key

  @property
  def _dict(self):
    return {
      tuple(stroke.split(STROKE_DELIMITER)): translation
      for (stroke, translation) in self._rtf_dict.stroke_to_translation.items()
    }

  @_dict.setter
  def _dict(self, new_val):
    pass

  @property
  def reverse(self):
    return {
      translation: [tuple(stroke.split(STROKE_DELIMITER)) for stroke in strokes]
      for (translation, strokes) in self._rtf_dict.translation_to_strokes.items()
    }

  @reverse.setter
  def reverse(self, new_val):
    pass

  def clear(self):
    self._rtf_dict = rtfcre.RtfDictionary()

  def lookup(self, steno):
    return self._rtf_dict.lookup(STROKE_DELIMITER.join(steno))

  def reverse_lookup(self, translation):
    return {
      tuple(stroke.split(STROKE_DELIMITER))
      for stroke in self._rtf_dict.reverse_lookup(translation)
    }
