# Crawler Shopee Tech Spec

# 1. Giới thiệu dự án

## Mô tả tổng quan

Dự án Shopee crawler là một công cụ mạnh mẽ được thiết kế để thu thập dữ liệu từ Shopee - một nền tảng thương mại điện tử phổ biến. Crawler sẽ tự động cào dữ liệu về cửa hàng, sản phẩm từ Shopee, lưu trữ thông tin theo thời gian thực và cung cấp các phân tích, báo cáo về thị trường.

## Mục tiêu

Mục tiêu chính của dự án Shopee crawler là cung cấp cho khách hàng một công cụ hiệu quả để thu thập và phân tích dữ liệu từ Shopee. Với sự trợ giúp của crawler, khách hàng có thể nắm bắt thông tin thị trường, cạnh tranh và xu hướng trong ngành thương mại điện tử, từ đó đưa ra các quyết định kinh doanh chiến lược.

## Phạm vi

Crawler của chúng tôi sẽ tập trung vào việc thu thập dữ liệu sản phẩm từ Shopee, bao gồm các thông tin như tên sản phẩm, tên cửa hàng, giá, mô tả, đánh giá, đặc điểm kỹ thuật và hình ảnh. Ngoài ra, chúng tôi cũng sẽ cung cấp khả năng lưu trữ dữ liệu theo thời gian thực với mục đích tạo ra các phân tích, báo cáo dựa trên dữ liệu đã thu thập được.

## Lợi ích

Dưới đây là một số lợi ích mà crawler của chúng tôi mang lại:

1. Tiết kiệm thời gian và công sức: Crawler tự động thu thập dữ liệu từ Shopee, giúp khách hàng tiết kiệm thời gian và công sức so với việc thủ công thu thập dữ liệu.
2. Độ chính xác và toàn diện: Crawler cung cấp dữ liệu chi tiết và đáng tin cậy từ Shopee, giúp khách hàng có cái nhìn toàn diện về thị trường và sản phẩm.
3. Phân tích cạnh tranh và xu hướng: Crawler giúp khách hàng xác định xu hướng và phân tích cạnh tranh trong ngành của mình. Điều này giúp họ nắm bắt được sự phát triển và tạo ra các kế hoạch kinh doanh chiến lược.
4. Lưu trữ và theo dõi thời gian thực: Crawler lưu trữ và cập nhật dữ liệu theo thời gian thực, giúp khách hàng theo dõi sự thay đổi và phát triển trên Shopee một cách liên tục.
5. Tùy chỉnh và linh hoạt: Crawler được thiết kế để linh hoạt và có thể tùy chỉnh theo yêu cầu cụ thể của khách hàng, từ việc lựa chọn dữ liệu cần thu thập đến cách lưu trữ và hiển thị kết quả.

Dự án crawler từ Shopee của chúng tôi là một công cụ mạnh mẽ giúp khách hàng nắm bắt thông tin thị trường, cạnh tranh và xu hướng trong ngành thương mại điện tử. Với sự trợ giúp của crawler, khách hàng có thể đưa ra các quyết định kinh doanh thông minh và nhanh chóng dựa trên dữ liệu chính xác và toàn diện.

# 2. Cài đặt và yêu cầu

## Yêu cầu hệ thống

Docker và Docker compose: Crawler của chúng tôi được thiết kế để chạy trong môi trường Docker. Vì vậy, khách hàng cần cài đặt Docker và Docker compose trên hệ thống của mình. Vui lòng tham khảo **[trang chủ Docker](https://www.docker.com/)** để cài đặt Docker và Docker compose cho hệ điều hành của bạn.

## Cài đặt

Để cài đặt crawler, hãy thực hiện từng bước như sau:

1. Tải mã nguồn: Khách hàng có thể tải mã nguồn của crawler từ [link](https://github.com/ColorMe-Bussiness-Development/social-scanner-crawler) hoặc sử dụng lệnh sau để sao chép mã nguồn từ repository:
    
    ```jsx
    git clone https://github.com/ColorMe-Bussiness-Development/social-scanner-crawler.git
    ```
    
    **Note**: Hãy đảm bảo rằng bạn có quyền truy cập vào repository.
    
2. Cấu hình môi trường:
    
    Để cấu hình crawler trong môi trường Docker, khách hàng cần tạo thay đổi các tùy chọn cấu hình trong tệp `.env`. Chúng tôi đã cung cấp một mẫu tệp cấu hình `.env.example` với các giá trị mặc định để khách hàng có thể tham khảo.
    
3. Triển khai crawler trong Docker: Sau khi đã thay đổi tệp cấu hình, sử dụng lệnh sau để triển khai crawler trong Docker
    
    ```jsx
    ./init.sh
    ```
    
    Để kiểm tra crawler đã được triển khai thành công chưa, sử dụng lệnh sau và kiểm tra trạng thái của container `social-scanner-crawler`
    
    ```jsx
    docker container ps
    ```
    

## Cách sử dụng

1. Connect vào container:
    
    ```jsx
    ./connect.sh
    ```
    
2. Lập lịch crawl data:
    
    ```jsx
    python src/app.py
    ```
    

Sau khi lập lịch, hệ thống sẽ crawl data theo lịch đã quy định trong file `src/app.py`

- Khách hàng có thể sử dụng lệnh sau để kiểm tra lịch crawl data:
    
    ```jsx
    crontab -l
    
    # Response example:
    # 0 0,12 * * * /usr/local/bin/python /crawler/src/job/shopee/collect_shop_flow_a.py
    # 0 0,12 * * * /usr/local/bin/python /crawler/src/job/shopee/collect_shop_flow_b.py
    # 0 0,12 * * * /usr/local/bin/python /crawler/src/job/shopee/get_shop_detail.py
    # 0 0,8,16 * * * /usr/local/bin/python /crawler/src/job/shopee/collect_product_in_shop.py
    # 0 0,8,16 * * * /usr/local/bin/python /crawler/src/job/shopee/collect_product_in_shop.py
    # @hourly /usr/local/bin/python /crawler/src/job/shopee/save_product_statistics.py
    # @hourly /usr/local/bin/python /crawler/src/job/shopee/save_shop_statistics.py
    # * * * * * /usr/local/bin/python /crawler/src/job/shopee/test.py
    ```
    
    **Chú thích:**
    
    `0 0,8,16 * * * /usr/local/bin/python /crawler/src/job/shopee/collect_product_in_shop.py` : Hệ thống sẽ chạy câu lệnh `/usr/local/bin/python /crawler/src/job/shopee/collect_product_in_shop.py` tại 0:00, 08:00, 16:00 mỗi ngày.
    
    Tham khảo thêm về contab tại [đây](https://www.ibm.com/docs/en/aix/7.2?topic=c-crontab-command)
    
- Để thay đổi lịch crawl data, khách hàng cần thực hiện những bước sau:
    1. Truy cập vào file quy định lịch crawl data
    
    ```jsx
    crontab -e
    ```
    
    1. Nhấn i để sử dụng chế độ edit
    2. Sửa đổi thời gian, command của lịch. Tham khảo thêm về crontab tại [đây](https://www.ibm.com/docs/en/aix/7.2?topic=c-crontab-command)
    3. Nhấn `esc` —> `:wq` để lưu thay đổi và thoát chế độ chỉnh sửa lịch

Khách hàng cũng có thể xem log của crawler ở thư mục `./log`

# 3. Cấu trúc và kiến trúc

## Cấu trúc tổng quan

Crawler của chúng tôi được thiết kế với một cấu trúc và kiến trúc phù hợp để thu thập dữ liệu từ Shopee một cách hiệu quả. Dưới đây là mô tả tổng quan về cấu trúc và các thành phần chính của crawler:

![diagram](https://github.com/ColorMe-Bussiness-Development/social-scanner-crawler/blob/411642831c29204a2f0cae512761e29bb87e81bf/diagram.png?raw=true)

1. Crawler: Đây là thành phần chính của dự án, nó chịu trách nhiệm thực hiện quá trình cào dữ liệu từ Shopee. Crawler được xây dựng với mục tiêu thu thập thông tin về sản phẩm, danh mục, giá cả, đánh giá và các thuộc tính khác từ trang web Shopee. Nó sử dụng các kỹ thuật và công nghệ để tự động duyệt qua các trang, lấy dữ liệu và lưu trữ chúng cho phân tích và sử dụng sau này.
2. Proxy: Đây là thành phần hỗ trợ trong dự án, chịu trách nhiệm tạo một lớp ẩn danh cho crawler khi cào dữ liệu từ Shopee. Proxy được sử dụng để che giấu địa chỉ IP thực của crawler, giúp bảo vệ danh tính và ngăn chặn các biện pháp hạn chế từ phía Shopee như chặn IP hoặc giới hạn tốc độ truy cập. Proxy giúp tăng tính ổn định và đảm bảo hoạt động liên tục của crawler trong quá trình thu thập dữ liệu.
3. Main database: Main database là một cơ sở dữ liệu quan trọng trong dự án, được sử dụng để lưu trữ và quản lý dữ liệu thu thập được từ Shopee. Dữ liệu về sản phẩm, danh mục, giá cả, đánh giá và các thuộc tính khác được cào từ Shopee sẽ được lưu trữ trong main database. Điều này cho phép khách hàng có thể truy xuất, truy vấn và sử dụng dữ liệu theo nhu cầu của họ để thực hiện các phân tích, báo cáo và xử lý dữ liệu sau này.
4. Timescale database: Timescale database là một cơ sở dữ liệu đặc biệt được sử dụng để lưu trữ và quản lý dữ liệu theo thời gian thực từ crawler. Đây là nơi lưu trữ các dữ liệu có tính chất chuỗi thời gian như lịch sử cập nhật sản phẩm, thay đổi giá cả theo thời gian và các hoạt động khác trên Shopee. Timescale database cung cấp cấu trúc tối ưu để lưu trữ và xử lý dữ liệu thời gian thực một cách hiệu quả, cho phép truy vấn và phân tích dữ liệu dễ dàng theo thời gian.

## Các thành phần chính

1. Module crawler: module crawler được chia thành 5 luồng hoạt động
    - Luồng 1: sưu tầm `shop_id`, `username` của official shop:
        - Đường dẫn: `./src/job/shopee/collect_shop_flow_a.py`
        - Mô tả: crawler tìm kiếm những official shop chưa tồn tại trong main database, lưu thông tin về shop_id, username của shop.
    - Luồng 2: sưu tầm shop_id, username của shop thông qua category:
        - Đường dẫn: `./src/job/shopee/collect_shop_flow_b.py`
        - Mô tả: crawler tìm kiếm những sản phẩm có liên quan đến category được chỉ định, trích xuất dữ liệu về shop của những sản phẩm đó, lưu thông tin về shop_id, username của shop vào main database nếu shop chưa tồn tại trong main database.
    - Luồng 3: cập nhật đầy đủ thông tin của shop:
        - Đường dẫn: `./src/job/shopee/get_shop_detail.py`
        - Mô tả: dựa vào những thông tin về shop_id, username thu thập được từ 2 luồng trên, crawler truy vấn đến shopee để cập nhật đầy đủ thông tin về shop.
    - Luồng 4: thu thập tất cả sản phẩm thuộc ngành mĩ phẩm của shop
        - Đường dẫn: `./src/job/shopee/collect_product_in_shop.py`
        - Mô tả: crawler cào toàn bộ product của từng shop trong main database, lọc những product của ngành mĩ phẩm và lưu/cập nhật thông tin của product vào main database.
    - Luồng 5: thu thập thông tin về brand, cây category của product
        - Đường dẫn: `./src/job/shopee/get_product_category.py`
        - Mô tả: vì dữ liệu của shopee trả về ở luồng 4 không có dữ liệu về brand và cây category của sản phẩm, nên crawler chạy luồng 5 để cập nhật brand, cây category của từng sản phẩm
2. Module lưu thông số (số lượt bán, giá trung bình, số lượt bình luận, …) của shop, product theo thời gian:
    - Luồng 1: Lưu thông số của product:
        - Đường dẫn: `./src/job/database/save_product_statistics.py`
        - Mô tả: Cứ sau 1 giờ, crawler sẽ tự động ghi lại bảng product của main database và lưu trữ vào bảng product_timescale của timescale database.
    - Luồng 2: Lưu thông số của shop:
        - Đường dẫn: `./src/job/database/save_shop_statistics.py`
        - Mô tả: Cứ sau 1 giờ, crawler sẽ tự động ghi lại bảng shop của main database và lưu trữ vào bảng shop_timescale của timescale database.
    - Luồng 3: Đồng bộ dữ liệu của bảng product_filter và shop_filter từ main database sang timescale database.
        - Đường dẫn: `./src/job/database/sync_filter_table.py`
        - Mô tả: Vì các bảng từ main database không thể join với các bảng từ timescale database, nên chúng tôi tạo ra 2 bảng product_filter và shop_filter nằm trong timescale database nhằm mục đích tăng tốc độ truy vấn dữ liệu. 2 bảng trên sẽ chứa những trường dữ liệu cần thiết để filter. Cứ sau 1 giờ, crawler sẽ kiểm tra những product mới, shop mới từ main database và đồng bộ những trường cần thiết vào 2 bảng product_filter và shop_filter trong timescale database.
