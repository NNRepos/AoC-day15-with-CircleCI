part1=__import__("15")
class Tester():
  
  def test_input0(self):
    input=part1.input
    assert part1.main(input, True) == 227290
  
  def test_input1(self):
    input=part1.input1
    assert part1.main(input, True) == 27730
  
  def test_input2(self):
    input=part1.input2
    assert part1.main(input, True) == 36334
  
  def test_input3(self):
    input=part1.input3
    assert part1.main(input, True) == 39514
  
  def test_input4(self):
    input=part1.input4
    assert part1.main(input, True) == 27755
  
  def test_input5(self):
    input=part1.input5
    assert part1.main(input, True) == 28944
  
  def test_input6(self):
    input=part1.input6
    assert part1.main(input, True) == 18740
  