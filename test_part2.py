part2=__import__("15^2")
class Tester():
  
  def test_input0(self):
    input=part2.input
    assert part2.main(input, True) == 53725
  
  def test_input1(self):
    input=part2.input1
    assert part2.main(input, True) == 4988
  
  def test_input2(self):
    input=part2.input2
    assert part2.main(input, True) == 31284
  
  def test_input3(self):
    input=part2.input3
    assert part2.main(input, True) == 3478
  
  def test_input4(self):
    input=part2.input4
    assert part2.main(input, True) == 6474
  
  def test_input5(self):
    input=part2.input5
    assert part2.main(input, True) == 1140