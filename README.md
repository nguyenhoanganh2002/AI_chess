# AI chess using Artificial Neural Network
Project kiểm tra ứng dụng của ANN trong việc xây dựng một chương trình cờ vua
### Các thư viện và ngôn ngữ sử dụng:
* `Python 3.10`: toàn bộ project đều sử dụng ngôn ngữ lập trình Python
* `Pygame`: lập trình ứng dụng và giao diện game
* `Python-chess`: hỗ trợ thao tác trên bàn cờ
* `Numpy`: xử lý dữ liệu số, dữ liệu dạng mảng,...
* `Tensorflow 2.0`: làm việc với mô hình ANN 
### Các folder và python file quan trọng
* Folder `ANN_for_Chess`: chứa file chuẩn bị tập dữ liệu `generate_dataset.ipynb`; huấn luyện mô hình `train.ipynb`; các mô hình tốt nhất được lưu trong folder `model` dưới dạng `.h5`. Do kích thước dữ liệu quá lớn nên tôi không thể push lên github. Thay vào đó nếu bạn muốn huấn luyện lại mô hình ANN, bạn có thể lấy dữ liệu thô ở https://www.ficsgames.org/download.html. Sau đấy điều chỉnh đường dẫn phù hợp và thực thi file `generate_dataset.ipynb`. Tiếp theo, bạn có thể thiết kế và huấn luyện lại mô hình ở file `train.ipynb`. Good luck!!
* `model.py`: convert Keras model sang Tensorflow Lite để tăng tốc độ predict của ANN model
* `computer.py`: triển khai giải thuật cắt tỉa alpha-beta kết hợp với ANN model để tìm nước đi tối ưu
* `ai.py`: triển khai giải thuật cắt tỉa alpha-beta với các heuristic cơ bản để kiểm thử sức mạnh của ANN
### Cách sử dụng
* Clone source code về và cài đặt các thư viện được trình bày ở trên
* Thực thi file `main.py`
### Thông tin liên lạc:
* Email: anh.nh204511@gmail.com


