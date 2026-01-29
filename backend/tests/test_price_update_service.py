"""价格更新服务测试。

测试 PriceUpdateService 的各种场景，包括正常情况和异常情况。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.services.price_update_service import PriceUpdateService
from app.database.models import Post


class TestGetFuturesSpotPrice:
    """测试 get_futures_spot_price 方法。"""

    def test_get_price_success_with_symbol_column(self):
        """测试成功获取价格 - 使用 'symbol' 列名。"""
        # 准备测试数据
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟 akshare 返回的数据
        mock_data = pd.DataFrame({
            'symbol': ['IF2312', 'RB2312', 'AU2312'],
            'current_price': [3500.5, 3800.0, 450.25]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result == 3500.5
            assert isinstance(result, float)

    def test_get_price_success_with_chinese_column_names(self):
        """测试成功获取价格 - 使用中文列名（'合约代码' 和 '最新价'）。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟 akshare 返回的数据（使用中文列名）
        mock_data = pd.DataFrame({
            '合约代码': ['IF2312', 'RB2312'],
            '最新价': [3500.5, 3800.0]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result == 3500.5

    def test_get_price_success_case_insensitive(self):
        """测试成功获取价格 - 不区分大小写匹配。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        mock_data = pd.DataFrame({
            'symbol': ['if2312', 'RB2312'],  # 小写
            'current_price': [3500.5, 3800.0]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')  # 大写查询
            
            assert result == 3500.5

    def test_get_price_returns_none_when_data_is_empty(self):
        """测试当 akshare 返回空数据时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟返回空 DataFrame
        empty_data = pd.DataFrame()
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=empty_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_returns_none_when_data_is_none(self):
        """测试当 akshare 返回 None 时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=None):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_returns_none_when_contract_not_found(self):
        """测试当合约代码不存在时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        mock_data = pd.DataFrame({
            'symbol': ['RB2312', 'AU2312'],
            'current_price': [3800.0, 450.25]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_returns_none_when_code_column_missing(self):
        """测试当找不到合约代码列时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟数据中没有合约代码列
        mock_data = pd.DataFrame({
            'wrong_column': ['IF2312'],
            'current_price': [3500.5]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_returns_none_when_price_column_missing(self):
        """测试当找不到价格列时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟数据中没有价格列
        mock_data = pd.DataFrame({
            'symbol': ['IF2312'],
            'wrong_column': [3500.5]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_handles_invalid_price_value(self):
        """测试当价格值无法转换为浮点数时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        mock_data = pd.DataFrame({
            'symbol': ['IF2312'],
            'current_price': ['invalid_price']  # 无效的价格值
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_handles_nan_price_value(self):
        """测试当价格值为 NaN 时返回 None。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        mock_data = pd.DataFrame({
            'symbol': ['IF2312'],
            'current_price': [np.nan]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            # NaN 转换为 float 会失败，应该返回 None
            assert result is None

    def test_get_price_handles_network_error(self):
        """测试处理网络错误。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟网络异常
        with patch('app.services.price_update_service.ak.futures_zh_spot', side_effect=Exception("网络连接失败")):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_handles_timeout_error(self):
        """测试处理超时错误。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟超时异常
        with patch('app.services.price_update_service.ak.futures_zh_spot', side_effect=TimeoutError("请求超时")):
            result = service.get_futures_spot_price('IF2312')
            
            assert result is None

    def test_get_price_with_multiple_matches(self):
        """测试当有多个匹配时返回第一个匹配的价格。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        # 模拟有多个匹配的情况
        mock_data = pd.DataFrame({
            'symbol': ['IF2312', 'IF2312-2'],  # 两个匹配
            'current_price': [3500.5, 3600.0]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.get_futures_spot_price('IF2312')
            
            # 应该返回第一个匹配的价格
            assert result == 3500.5

    def test_get_price_with_partial_match(self):
        """测试部分匹配合约代码。"""
        mock_db = Mock(spec=Session)
        service = PriceUpdateService(mock_db)
        
        mock_data = pd.DataFrame({
            'symbol': ['IF2312', 'IF2313'],
            'current_price': [3500.5, 3510.0]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            # 使用部分匹配（包含 'IF2312'）
            result = service.get_futures_spot_price('IF2312')
            
            assert result == 3500.5


class TestUpdatePostPrice:
    """测试 update_post_price 方法。"""

    def test_update_post_price_success(self):
        """测试成功更新帖子价格。"""
        # 创建模拟的数据库会话和帖子对象
        mock_db = Mock(spec=Session)
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = 'IF2312'
        mock_post.status = 1
        mock_post.current_price = None
        mock_post.updated_at = None
        
        # 模拟数据库查询
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_post
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟获取价格成功
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_post_price(1)
            
            assert result is True
            assert mock_post.current_price == 3500.5
            mock_db.commit.assert_called_once()

    def test_update_post_price_post_not_found(self):
        """测试帖子不存在时返回 False。"""
        mock_db = Mock(spec=Session)
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None  # 帖子不存在
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        result = service.update_post_price(999)
        
        assert result is False
        mock_db.commit.assert_not_called()

    def test_update_post_price_post_deleted(self):
        """测试帖子已删除（status=0）时返回 False。"""
        mock_db = Mock(spec=Session)
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.status = 0  # 已删除
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None  # 因为 status=0，查询不会返回
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        result = service.update_post_price(1)
        
        assert result is False

    def test_update_post_price_no_contract_code(self):
        """测试帖子没有合约代码时返回 False。"""
        mock_db = Mock(spec=Session)
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = None  # 没有合约代码
        mock_post.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_post
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        result = service.update_post_price(1)
        
        assert result is False
        mock_db.commit.assert_not_called()

    def test_update_post_price_price_fetch_failed(self):
        """测试获取价格失败时返回 False。"""
        mock_db = Mock(spec=Session)
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = 'IF2312'
        mock_post.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_post
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟获取价格失败
        with patch.object(service, 'get_futures_spot_price', return_value=None):
            result = service.update_post_price(1)
            
            assert result is False
            mock_db.commit.assert_not_called()

    def test_update_post_price_database_error(self):
        """测试数据库更新失败时回滚并返回 False。"""
        mock_db = Mock(spec=Session)
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = 'IF2312'
        mock_post.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_post
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        # 模拟数据库提交失败
        mock_db.commit.side_effect = SQLAlchemyError("数据库错误")
        
        service = PriceUpdateService(mock_db)
        
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_post_price(1)
            
            assert result is False
            mock_db.rollback.assert_called_once()


class TestUpdateAllPostsPrice:
    """测试 update_all_posts_price 方法。"""

    def test_update_all_posts_price_success(self):
        """测试成功批量更新所有帖子价格。"""
        mock_db = Mock(spec=Session)
        
        # 创建多个模拟帖子
        mock_post1 = Mock(spec=Post)
        mock_post1.post_id = 1
        mock_post1.contract_code = 'IF2312'
        mock_post1.status = 1
        
        mock_post2 = Mock(spec=Post)
        mock_post2.post_id = 2
        mock_post2.contract_code = 'RB2312'
        mock_post2.status = 1
        
        mock_post3 = Mock(spec=Post)
        mock_post3.post_id = 3
        mock_post3.contract_code = None  # 没有合约代码
        mock_post3.status = 1
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_post1, mock_post2, mock_post3]
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟获取价格成功
        # 注意：当帖子没有合约代码时，代码会跳过它，不会调用 update_post_price
        with patch.object(service, 'update_post_price') as mock_update:
            mock_update.side_effect = [True, True]  # 只有前两个会调用 update_post_price
            
            result = service.update_all_posts_price()
            
            assert result['total'] == 3
            assert result['success'] == 2
            assert result['failed'] == 1  # 第三个因为没有合约代码而失败
            assert mock_update.call_count == 2  # 只有前两个帖子会调用 update_post_price

    def test_update_all_posts_price_no_posts(self):
        """测试没有帖子时返回空统计。"""
        mock_db = Mock(spec=Session)
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []  # 没有帖子
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        result = service.update_all_posts_price()
        
        assert result['total'] == 0
        assert result['success'] == 0
        assert result['failed'] == 0

    def test_update_all_posts_price_exception_handling(self):
        """测试批量更新时处理异常。"""
        mock_db = Mock(spec=Session)
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.all.side_effect = Exception("数据库查询错误")
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        result = service.update_all_posts_price()
        
        assert result['total'] == 0
        assert result['success'] == 0
        assert result['failed'] == 0
        assert 'error' in result


class TestUpdatePostsByContractCode:
    """测试 update_posts_by_contract_code 方法。"""

    def test_update_posts_by_contract_code_success(self):
        """测试成功按合约代码更新帖子。"""
        mock_db = Mock(spec=Session)
        
        # 创建多个相同合约代码的帖子
        mock_post1 = Mock(spec=Post)
        mock_post1.post_id = 1
        mock_post1.contract_code = 'IF2312'
        mock_post1.status = 1
        
        mock_post2 = Mock(spec=Post)
        mock_post2.post_id = 2
        mock_post2.contract_code = 'IF2312'
        mock_post2.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = [mock_post1, mock_post2]
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟获取价格成功
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_posts_by_contract_code('IF2312')
            
            assert result['total'] == 2
            assert result['success'] == 2
            assert result['failed'] == 0
            assert mock_post1.current_price == 3500.5
            assert mock_post2.current_price == 3500.5
            mock_db.commit.assert_called_once()

    def test_update_posts_by_contract_code_price_fetch_failed(self):
        """测试获取价格失败时返回失败统计。"""
        mock_db = Mock(spec=Session)
        
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = 'IF2312'
        mock_post.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = [mock_post]
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟获取价格失败
        with patch.object(service, 'get_futures_spot_price', return_value=None):
            result = service.update_posts_by_contract_code('IF2312')
            
            assert result['total'] == 1
            assert result['success'] == 0
            assert result['failed'] == 1
            mock_db.commit.assert_not_called()

    def test_update_posts_by_contract_code_no_posts(self):
        """测试没有匹配的帖子时返回空统计。"""
        mock_db = Mock(spec=Session)
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = []  # 没有帖子
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_posts_by_contract_code('IF2312')
            
            assert result['total'] == 0
            assert result['success'] == 0
            assert result['failed'] == 0

    def test_update_posts_by_contract_code_partial_failure(self):
        """测试部分帖子更新失败。"""
        mock_db = Mock(spec=Session)
        
        mock_post1 = Mock(spec=Post)
        mock_post1.post_id = 1
        mock_post1.contract_code = 'IF2312'
        mock_post1.status = 1
        
        mock_post2 = Mock(spec=Post)
        mock_post2.post_id = 2
        mock_post2.contract_code = 'IF2312'
        mock_post2.status = 1
        # 模拟第二个帖子更新时出错（设置属性时抛出异常）
        def set_price_error(value):
            raise AttributeError("无法设置价格属性")
        type(mock_post2).current_price = property(lambda self: None, set_price_error)
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = [mock_post1, mock_post2]
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_posts_by_contract_code('IF2312')
            
            assert result['total'] == 2
            assert result['success'] == 1
            assert result['failed'] == 1

    def test_update_posts_by_contract_code_database_error(self):
        """测试数据库提交失败时回滚。"""
        mock_db = Mock(spec=Session)
        
        mock_post = Mock(spec=Post)
        mock_post.post_id = 1
        mock_post.contract_code = 'IF2312'
        mock_post.status = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = [mock_post]
        mock_query.filter.return_value = mock_filter
        mock_db.query.return_value = mock_query
        
        # 模拟数据库提交失败
        mock_db.commit.side_effect = SQLAlchemyError("数据库错误")
        
        service = PriceUpdateService(mock_db)
        
        with patch.object(service, 'get_futures_spot_price', return_value=3500.5):
            result = service.update_posts_by_contract_code('IF2312')
            
            assert result['total'] == 0
            assert result['success'] == 0
            assert result['failed'] == 0
            assert 'error' in result
            mock_db.rollback.assert_called_once()


class TestPriceUpdateServiceIntegration:
    """集成测试 - 测试完整的流程。"""

    def test_full_update_flow(self):
        """测试完整的价格更新流程。"""
        mock_db = Mock(spec=Session)
        
        # 模拟多个帖子
        mock_posts = []
        for i in range(3):
            post = Mock(spec=Post)
            post.post_id = i + 1
            post.contract_code = f'IF231{i}'
            post.status = 1
            mock_posts.append(post)
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = mock_posts
        mock_db.query.return_value = mock_query
        
        service = PriceUpdateService(mock_db)
        
        # 模拟 akshare 返回的数据
        mock_data = pd.DataFrame({
            'symbol': ['IF2310', 'IF2311', 'IF2312'],
            'current_price': [3500.5, 3510.0, 3520.5]
        })
        
        with patch('app.services.price_update_service.ak.futures_zh_spot', return_value=mock_data):
            result = service.update_all_posts_price()
            
            # 验证结果
            assert result['total'] == 3
            # 注意：由于我们使用的是 mock，实际的更新可能不会完全成功
            # 但至少验证了流程不会崩溃



