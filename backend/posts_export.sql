-- 期货数据导出
-- 导出时间: 2026-01-01T20:24:26.345984
-- 数据条数: 393

-- 先删除可能存在的重复数据（根据 contract_code 和 title）
DELETE FROM posts WHERE contract_code IS NOT NULL AND title IS NOT NULL;

-- 插入数据
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('集运欧线2604', 'EC2604', '期货合约 EC2604 的交易建议。

品种代码: EC
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.186615', '2026-01-02T08:49:50.421324', '2026-01-02T08:49:50.421324');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('集运欧线2606', 'EC2606', '期货合约 EC2606 的交易建议。

品种代码: EC
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.193251', '2026-01-02T08:49:51.190995', '2026-01-02T08:49:51.190995');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('中证5002601', 'IC2601', '期货合约 IC2601 的交易建议。

品种代码: IC
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.196410', '2026-01-02T08:49:51.194944', '2026-01-02T08:49:51.194944');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沪深3002601', 'IF2601', '期货合约 IF2601 的交易建议。

品种代码: IF
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.199162', '2026-01-02T08:49:51.197751', '2026-01-02T08:49:51.197751');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('上证502601', 'IH2601', '期货合约 IH2601 的交易建议。

品种代码: IH
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.202054', '2026-01-02T08:49:51.200377', '2026-01-02T08:49:51.200377');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('中证10002601', 'IM2601', '期货合约 IM2601 的交易建议。

品种代码: IM
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.204969', '2026-01-02T08:49:51.203417', '2026-01-02T08:49:51.203417');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('原木2605', 'LG2605', '期货合约 LG2605 的交易建议。

品种代码: LG
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.207657', '2026-01-02T08:49:51.206237', '2026-01-02T08:49:51.206237');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2603 (I2603)', 'I2603', '期货合约 I2603 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.280205', '2026-01-02T07:29:27.279682', '2026-01-02T08:41:39.378874');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2607 (I2607)', 'I2607', '期货合约 I2607 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.285873', '2026-01-02T07:29:27.284873', '2026-01-02T08:41:39.384697');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2611 (I2611)', 'I2611', '期货合约 I2611 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.292760', '2026-01-02T07:29:27.292319', '2026-01-02T08:41:39.390493');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('原木2607', 'LG2607', '期货合约 LG2607 的交易建议。

品种代码: LG
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.211701', '2026-01-02T08:49:51.208833', '2026-01-02T08:49:51.208833');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('低硫燃料油2603', 'LU2603', '期货合约 LU2603 的交易建议。

品种代码: LU
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.214759', '2026-01-02T08:49:51.213178', '2026-01-02T08:49:51.213178');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('瓶片2605', 'PR2605', '期货合约 PR2605 的交易建议。

品种代码: PR
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.217839', '2026-01-02T08:49:51.216315', '2026-01-02T08:49:51.216315');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SC2603', 'SC2603', '期货合约 SC2603 的交易建议。

品种代码: SC

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T07:07:27.342248', '2026-01-02T07:07:27.341797', '2026-01-02T08:41:39.068541');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SC2606', 'SC2606', '期货合约 SC2606 的交易建议。

品种代码: SC

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T07:07:27.344066', '2026-01-02T07:07:27.343760', '2026-01-02T08:41:39.071489');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SC2609', 'SC2609', '期货合约 SC2609 的交易建议。

品种代码: SC

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T07:07:27.345718', '2026-01-02T07:07:27.345346', '2026-01-02T08:41:39.076139');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SC2612', 'SC2612', '期货合约 SC2612 的交易建议。

品种代码: SC

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T07:07:27.347551', '2026-01-02T07:07:27.347189', '2026-01-02T08:41:39.079481');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2601 (C2601)', 'C2601', '期货合约 C2601 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.055665', '2026-01-02T07:29:27.055232', '2026-01-02T08:41:39.082629');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2605 (C2605)', 'C2605', '期货合约 C2605 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.066118', '2026-01-02T07:29:27.065695', '2026-01-02T08:41:39.088554');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2609 (C2609)', 'C2609', '期货合约 C2609 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.069710', '2026-01-02T07:29:27.069342', '2026-01-02T08:41:39.093434');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2612 (C2612)', 'C2612', '期货合约 C2612 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.075802', '2026-01-02T07:29:27.075392', '2026-01-02T08:41:39.098396');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2601 (M2601)', 'M2601', '期货合约 M2601 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.106509', '2026-01-02T07:29:27.106056', '2026-01-02T08:41:39.123935');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2605 (M2605)', 'M2605', '期货合约 M2605 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.111720', '2026-01-02T07:29:27.110492', '2026-01-02T08:41:39.129321');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2609 (M2609)', 'M2609', '期货合约 M2609 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.116720', '2026-01-02T07:29:27.116220', '2026-01-02T08:41:39.136891');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2612 (M2612)', 'M2612', '期货合约 M2612 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.122635', '2026-01-02T07:29:27.122241', '2026-01-02T08:41:39.141873');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2603 (Y2603)', 'Y2603', '期货合约 Y2603 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.127694', '2026-01-02T07:29:27.127278', '2026-01-02T08:41:39.147778');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2607 (Y2607)', 'Y2607', '期货合约 Y2607 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.137896', '2026-01-02T07:29:27.137205', '2026-01-02T08:41:39.153892');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2611 (Y2611)', 'Y2611', '期货合约 Y2611 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.142584', '2026-01-02T07:29:27.142213', '2026-01-02T08:41:39.160507');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2601 (P2601)', 'P2601', '期货合约 P2601 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.151722', '2026-01-02T07:29:27.151265', '2026-01-02T08:41:39.167285');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2605 (P2605)', 'P2605', '期货合约 P2605 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.166443', '2026-01-02T07:29:27.165796', '2026-01-02T08:41:39.175484');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2609 (P2609)', 'P2609', '期货合约 P2609 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.174953', '2026-01-02T07:29:27.174205', '2026-01-02T08:41:39.184990');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2612 (P2612)', 'P2612', '期货合约 P2612 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.181271', '2026-01-02T07:29:27.180675', '2026-01-02T08:41:39.200347');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2601 (L2601)', 'L2601', '期货合约 L2601 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.213280', '2026-01-02T07:29:27.212945', '2026-01-02T08:41:39.233168');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2605 (L2605)', 'L2605', '期货合约 L2605 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.216813', '2026-01-02T07:29:27.216484', '2026-01-02T08:41:39.241262');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('多晶硅2605', 'PS2605', '期货合约 PS2605 的交易建议。

品种代码: PS
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.221174', '2026-01-02T08:49:51.219669', '2026-01-02T08:49:51.219669');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铂金2606', 'PT2606', '期货合约 PT2606 的交易建议。

品种代码: PT
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.224276', '2026-01-02T08:49:51.222637', '2026-01-02T08:49:51.222637');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2603 (C2603)', 'C2603', '期货合约 C2603 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.061967', '2026-01-02T07:29:27.061366', '2026-01-02T08:41:39.085612');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2607 (C2607)', 'C2607', '期货合约 C2607 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.067876', '2026-01-02T07:29:27.067505', '2026-01-02T08:41:39.090997');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('玉米2611 (C2611)', 'C2611', '期货合约 C2611 的交易建议。

品种代码: C

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.073002', '2026-01-02T07:29:27.072540', '2026-01-02T08:41:39.095885');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2603 (M2603)', 'M2603', '期货合约 M2603 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.108928', '2026-01-02T07:29:27.108383', '2026-01-02T08:41:39.126449');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2607 (M2607)', 'M2607', '期货合约 M2607 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.113909', '2026-01-02T07:29:27.113524', '2026-01-02T08:41:39.134109');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆粕2611 (M2611)', 'M2611', '期货合约 M2611 的交易建议。

品种代码: M

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.120670', '2026-01-02T07:29:27.119347', '2026-01-02T08:41:39.139451');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2601 (Y2601)', 'Y2601', '期货合约 Y2601 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.125233', '2026-01-02T07:29:27.124343', '2026-01-02T08:41:39.144317');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2605 (Y2605)', 'Y2605', '期货合约 Y2605 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.131777', '2026-01-02T07:29:27.131146', '2026-01-02T08:41:39.150931');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2609 (Y2609)', 'Y2609', '期货合约 Y2609 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.140344', '2026-01-02T07:29:27.139875', '2026-01-02T08:41:39.157253');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆油2612 (Y2612)', 'Y2612', '期货合约 Y2612 的交易建议。

品种代码: Y

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.145216', '2026-01-02T07:29:27.144732', '2026-01-02T08:41:39.163725');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2603 (P2603)', 'P2603', '期货合约 P2603 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.155965', '2026-01-02T07:29:27.155334', '2026-01-02T08:41:39.170926');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2607 (P2607)', 'P2607', '期货合约 P2607 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.171985', '2026-01-02T07:29:27.169099', '2026-01-02T08:41:39.181679');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棕榈油2611 (P2611)', 'P2611', '期货合约 P2611 的交易建议。

品种代码: P

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.177557', '2026-01-02T07:29:27.177075', '2026-01-02T08:41:39.191883');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2603 (L2603)', 'L2603', '期货合约 L2603 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.215079', '2026-01-02T07:29:27.214636', '2026-01-02T08:41:39.237388');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2607 (L2607)', 'L2607', '期货合约 L2607 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.218437', '2026-01-02T07:29:27.218116', '2026-01-02T08:41:39.244644');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2611 (L2611)', 'L2611', '期货合约 L2611 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.221806', '2026-01-02T07:29:27.221517', '2026-01-02T08:41:39.252346');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2601 (V2601)', 'V2601', '期货合约 V2601 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.225242', '2026-01-02T07:29:27.224906', '2026-01-02T08:41:39.258807');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2605 (V2605)', 'V2605', '期货合约 V2605 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.228340', '2026-01-02T07:29:27.227961', '2026-01-02T08:41:39.277727');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2609 (V2609)', 'V2609', '期货合约 V2609 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.231353', '2026-01-02T07:29:27.231069', '2026-01-02T08:41:39.283832');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2612 (V2612)', 'V2612', '期货合约 V2612 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.235256', '2026-01-02T07:29:27.234616', '2026-01-02T08:41:39.290779');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('原油2602', 'SC2602', '期货合约 SC2602 的交易建议。

品种代码: SC
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.230274', '2026-01-02T08:49:51.225687', '2026-01-02T08:49:51.225687');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2609 (L2609)', 'L2609', '期货合约 L2609 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.220079', '2026-01-02T07:29:27.219776', '2026-01-02T08:41:39.249345');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('塑料2612 (L2612)', 'L2612', '期货合约 L2612 的交易建议。

品种代码: L

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.223585', '2026-01-02T07:29:27.223264', '2026-01-02T08:41:39.255892');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2603 (V2603)', 'V2603', '期货合约 V2603 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.226700', '2026-01-02T07:29:27.226414', '2026-01-02T08:41:39.273741');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2607 (V2607)', 'V2607', '期货合约 V2607 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.229856', '2026-01-02T07:29:27.229579', '2026-01-02T08:41:39.280783');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PVC2611 (V2611)', 'V2611', '期货合约 V2611 的交易建议。

品种代码: V

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.232686', '2026-01-02T07:29:27.232409', '2026-01-02T08:41:39.287218');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2603 (J2603)', 'J2603', '期货合约 J2603 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.256541', '2026-01-02T07:29:27.256283', '2026-01-02T08:41:39.329616');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2607 (J2607)', 'J2607', '期货合约 J2607 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.259528', '2026-01-02T07:29:27.259204', '2026-01-02T08:41:39.336427');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2611 (J2611)', 'J2611', '期货合约 J2611 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.262481', '2026-01-02T07:29:27.262180', '2026-01-02T08:41:39.343260');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('30年期国债2603', 'TL2603', '期货合约 TL2603 的交易建议。

品种代码: TL
当前价格: N/A（使用主力合约价格）

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:51.233255', '2026-01-02T08:49:51.231790', '2026-01-02T08:49:51.231790');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2605 (PG2605)', 'PG2605', '期货合约 PG2605 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.336118', '2026-01-02T07:29:27.335734', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2605 (PM2605)', 'PM2605', '期货合约 PM2605 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.381039', '2026-01-02T07:29:27.379871', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2607 (PM2607)', 'PM2607', '期货合约 PM2607 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.383876', '2026-01-02T07:29:27.383434', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2601 (J2601)', 'J2601', '期货合约 J2601 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.254979', '2026-01-02T07:29:27.254624', '2026-01-02T08:41:39.326237');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2605 (J2605)', 'J2605', '期货合约 J2605 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.257790', '2026-01-02T07:29:27.257541', '2026-01-02T08:41:39.332772');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2609 (J2609)', 'J2609', '期货合约 J2609 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.261009', '2026-01-02T07:29:27.260672', '2026-01-02T08:41:39.340217');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦炭2612 (J2612)', 'J2612', '期货合约 J2612 的交易建议。

品种代码: J

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.264306', '2026-01-02T07:29:27.263853', '2026-01-02T08:41:39.346836');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2601 (I2601)', 'I2601', '期货合约 I2601 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.276382', '2026-01-02T07:29:27.276113', '2026-01-02T08:41:39.375571');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2605 (I2605)', 'I2605', '期货合约 I2605 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.282908', '2026-01-02T07:29:27.282380', '2026-01-02T08:41:39.381972');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2609 (I2609)', 'I2609', '期货合约 I2609 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.289942', '2026-01-02T07:29:27.289056', '2026-01-02T08:41:39.387762');
INSERT INTO posts (title, contract_code, content, stop_loss, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铁矿石2612 (I2612)', 'I2612', '期货合约 I2612 的交易建议。

品种代码: I

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 0.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.295771', '2026-01-02T07:29:27.295236', '2026-01-02T08:41:39.393523');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2605', 'TA2605', '期货合约 TA2605 的交易建议。

品种代码: T
当前价格: 5110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4854.50, 5110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.604188', '2026-01-02T06:43:57.754762', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2601 (EG2601)', 'EG2601', '期货合约 EG2601 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.298466', '2026-01-02T07:29:27.297818', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2603 (EG2603)', 'EG2603', '期货合约 EG2603 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.302035', '2026-01-02T07:29:27.300500', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2605 (EG2605)', 'EG2605', '期货合约 EG2605 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.305492', '2026-01-02T07:29:27.305086', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2607 (EG2607)', 'EG2607', '期货合约 EG2607 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.307610', '2026-01-02T07:29:27.307107', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2609 (EG2609)', 'EG2609', '期货合约 EG2609 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.309360', '2026-01-02T07:29:27.308994', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2607', 'OI2607', '期货合约 OI2607 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.437731', '2026-01-02T07:29:27.437468', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2609', 'OI2609', '期货合约 OI2609 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.438978', '2026-01-02T07:29:27.438737', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2611', 'OI2611', '期货合约 OI2611 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.440392', '2026-01-02T07:29:27.440092', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2612', 'OI2612', '期货合约 OI2612 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.442001', '2026-01-02T07:29:27.441712', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2601 (MA2601)', 'MA2601', '期货合约 MA2601 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.443841', '2026-01-02T07:29:27.443371', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2603 (MA2603)', 'MA2603', '期货合约 MA2603 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.445521', '2026-01-02T07:29:27.445254', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2605 (MA2605)', 'MA2605', '期货合约 MA2605 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.447279', '2026-01-02T07:29:27.446964', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2611 (JM2611)', 'JM2611', '期货合约 JM2611 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.273556', '2026-01-02T07:29:27.273285', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2612 (JM2612)', 'JM2612', '期货合约 JM2612 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.274828', '2026-01-02T07:29:27.274581', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2607 (PG2607)', 'PG2607', '期货合约 PG2607 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.337558', '2026-01-02T07:29:27.337294', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2605 (WH2605)', 'WH2605', '期货合约 WH2605 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.364073', '2026-01-02T07:29:27.363640', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2609 (PM2609)', 'PM2609', '期货合约 PM2609 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.385654', '2026-01-02T07:29:27.385244', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2601 (SR2601)', 'SR2601', '期货合约 SR2601 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.407012', '2026-01-02T07:29:27.406432', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2607 (SR2607)', 'SR2607', '期货合约 SR2607 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.423253', '2026-01-02T07:29:27.421876', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2609 (SR2609)', 'SR2609', '期货合约 SR2609 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.425530', '2026-01-02T07:29:27.425096', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2611 (SR2611)', 'SR2611', '期货合约 SR2611 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.427587', '2026-01-02T07:29:27.427171', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2612 (SR2612)', 'SR2612', '期货合约 SR2612 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.431192', '2026-01-02T07:29:27.430458', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2603', 'OI2603', '期货合约 OI2603 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.434830', '2026-01-02T07:29:27.434510', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2605', 'OI2605', '期货合约 OI2605 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.436199', '2026-01-02T07:29:27.435940', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2605 (PP2605)', 'PP2605', '期货合约 PP2605 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.243792', '2026-01-02T07:29:27.243374', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2607 (PP2607)', 'PP2607', '期货合约 PP2607 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.247559', '2026-01-02T07:29:27.247011', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2609 (PP2609)', 'PP2609', '期货合约 PP2609 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.250152', '2026-01-02T07:29:27.249686', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2611 (PP2611)', 'PP2611', '期货合约 PP2611 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.251819', '2026-01-02T07:29:27.251540', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2612 (PP2612)', 'PP2612', '期货合约 PP2612 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.253505', '2026-01-02T07:29:27.253224', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2601 (JM2601)', 'JM2601', '期货合约 JM2601 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.265967', '2026-01-02T07:29:27.265646', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2603 (JM2603)', 'JM2603', '期货合约 JM2603 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.267729', '2026-01-02T07:29:27.267305', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2605 (JM2605)', 'JM2605', '期货合约 JM2605 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.269215', '2026-01-02T07:29:27.268952', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2607 (JM2607)', 'JM2607', '期货合约 JM2607 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.270795', '2026-01-02T07:29:27.270511', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('焦煤2609 (JM2609)', 'JM2609', '期货合约 JM2609 的交易建议。

品种代码: JM
当前价格: 1804.5

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1714.27, 1804.50, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.272137', '2026-01-02T07:29:27.271888', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2607 (MA2607)', 'MA2607', '期货合约 MA2607 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.448704', '2026-01-02T07:29:27.448387', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2609 (MA2609)', 'MA2609', '期货合约 MA2609 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.478712', '2026-01-02T07:29:27.477886', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2611 (MA2611)', 'MA2611', '期货合约 MA2611 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.482139', '2026-01-02T07:29:27.481090', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('甲醇2612 (MA2612)', 'MA2612', '期货合约 MA2612 的交易建议。

品种代码: MA
当前价格: 2556.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2428.20, 2556.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.484970', '2026-01-02T07:29:27.484537', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2601', 'FG2601', '期货合约 FG2601 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.489613', '2026-01-02T07:29:27.488747', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2603', 'TA2603', '期货合约 TA2603 的交易建议。

品种代码: T
当前价格: 5098.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4843.10, 5098.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.617366', '2026-01-02T06:43:58.616497', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2602', 'TA2602', '期货合约 TA2602 的交易建议。

品种代码: T
当前价格: 5084.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4829.80, 5084.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.620927', '2026-01-02T06:43:58.620495', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2601', 'TA2601', '期货合约 TA2601 的交易建议。

品种代码: T
当前价格: 5066.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4812.70, 5066.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.623010', '2026-01-02T06:43:58.622568', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2604', 'TA2604', '期货合约 TA2604 的交易建议。

品种代码: T
当前价格: 5100.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4845.00, 5100.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.624859', '2026-01-02T06:43:58.624521', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2610', 'TA2610', '期货合约 TA2610 的交易建议。

品种代码: T
当前价格: 5028.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4776.60, 5028.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.627398', '2026-01-02T06:43:58.626950', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2606', 'TA2606', '期货合约 TA2606 的交易建议。

品种代码: T
当前价格: 5096.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4841.20, 5096.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.632514', '2026-01-02T06:43:58.629121', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2607', 'TA2607', '期货合约 TA2607 的交易建议。

品种代码: T
当前价格: 5068.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4814.60, 5068.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.635773', '2026-01-02T06:43:58.635203', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2612', 'TA2612', '期货合约 TA2612 的交易建议。

品种代码: T
当前价格: 5036.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4784.20, 5036.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.643811', '2026-01-02T06:43:58.642924', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2611', 'TA2611', '期货合约 TA2611 的交易建议。

品种代码: T
当前价格: 5032.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4780.40, 5032.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.652468', '2026-01-02T06:43:58.651777', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2603 (BU2603)', 'BU2603', '期货合约 BU2603 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T07:07:27.340018', '2026-01-02T07:07:27.339549', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2601 (A2601)', 'A2601', '期货合约 A2601 的交易建议。

品种代码: A
当前价格: 5066.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4812.70, 5066.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.078011', '2026-01-02T07:29:27.077606', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('OI2601', 'OI2601', '期货合约 OI2601 的交易建议。

品种代码: OI
当前价格: 8478.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8054.10, 8478.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.433246', '2026-01-02T07:29:27.432940', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2603', 'FG2603', '期货合约 FG2603 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.492091', '2026-01-02T07:29:27.491546', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2605', 'FG2605', '期货合约 FG2605 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.498921', '2026-01-02T07:29:27.498144', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PTA2609', 'TA2609', '期货合约 TA2609 的交易建议。

品种代码: T
当前价格: 5010.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4759.50, 5010.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:43:58.612734', '2026-01-02T06:43:58.612001', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2603 (WH2603)', 'WH2603', '期货合约 WH2603 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.361870', '2026-01-02T07:29:27.360747', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2607 (WH2607)', 'WH2607', '期货合约 WH2607 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.366189', '2026-01-02T07:29:27.365836', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2609 (WH2609)', 'WH2609', '期货合约 WH2609 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.369153', '2026-01-02T07:29:27.367831', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2611 (WH2611)', 'WH2611', '期货合约 WH2611 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.371394', '2026-01-02T07:29:27.370949', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2603 (PM2603)', 'PM2603', '期货合约 PM2603 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.376922', '2026-01-02T07:29:27.376518', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2611 (PM2611)', 'PM2611', '期货合约 PM2611 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.387817', '2026-01-02T07:29:27.387366', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2605 (CF2605)', 'CF2605', '期货合约 CF2605 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.395377', '2026-01-02T07:29:27.394868', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2607 (CF2607)', 'CF2607', '期货合约 CF2607 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.396961', '2026-01-02T07:29:27.396618', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2609 (CF2609)', 'CF2609', '期货合约 CF2609 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.398891', '2026-01-02T07:29:27.398463', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2611 (CF2611)', 'CF2611', '期货合约 CF2611 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.401318', '2026-01-02T07:29:27.400877', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2612 (CF2612)', 'CF2612', '期货合约 CF2612 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.404479', '2026-01-02T07:29:27.403835', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2607', 'FG2607', '期货合约 FG2607 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.506374', '2026-01-02T07:29:27.505320', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2612 (JD2612)', 'JD2612', '期货合约 JD2612 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.211526', '2026-01-02T07:29:27.211221', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2601 (PP2601)', 'PP2601', '期货合约 PP2601 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.238743', '2026-01-02T07:29:27.238235', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('聚丙烯2603 (PP2603)', 'PP2603', '期货合约 PP2603 的交易建议。

品种代码: PP
当前价格: 7629.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7247.55, 7629.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.241821', '2026-01-02T07:29:27.241354', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2605 (SR2605)', 'SR2605', '期货合约 SR2605 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.412738', '2026-01-02T07:29:27.412274', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2609', 'FG2609', '期货合约 FG2609 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.510528', '2026-01-02T07:29:27.509385', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2611', 'FG2611', '期货合约 FG2611 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.514383', '2026-01-02T07:29:27.513806', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('FG2612', 'FG2612', '期货合约 FG2612 的交易建议。

品种代码: FG
当前价格: 1551.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1473.45, 1551.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.517178', '2026-01-02T07:29:27.516670', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2601', 'RM2601', '期货合约 RM2601 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.520649', '2026-01-02T07:29:27.519202', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2603', 'RM2603', '期货合约 RM2603 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.523550', '2026-01-02T07:29:27.522628', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2605', 'RM2605', '期货合约 RM2605 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.525965', '2026-01-02T07:29:27.525514', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2607', 'RM2607', '期货合约 RM2607 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.530601', '2026-01-02T07:29:27.530122', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2609', 'RM2609', '期货合约 RM2609 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.533735', '2026-01-02T07:29:27.533212', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2611', 'RM2611', '期货合约 RM2611 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.537393', '2026-01-02T07:29:27.535792', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('RM2612', 'RM2612', '期货合约 RM2612 的交易建议。

品种代码: RM
当前价格: 2774.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2635.30, 2774.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.540387', '2026-01-02T07:29:27.539748', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2601 (SF2601)', 'SF2601', '期货合约 SF2601 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.543287', '2026-01-02T07:29:27.542643', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2603 (SF2603)', 'SF2603', '期货合约 SF2603 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.546958', '2026-01-02T07:29:27.546482', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2605 (SF2605)', 'SF2605', '期货合约 SF2605 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.549928', '2026-01-02T07:29:27.548749', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2607 (SF2607)', 'SF2607', '期货合约 SF2607 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.555588', '2026-01-02T07:29:27.554988', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2609 (SF2609)', 'SF2609', '期货合约 SF2609 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.558713', '2026-01-02T07:29:27.557731', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2611 (SF2611)', 'SF2611', '期货合约 SF2611 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.566697', '2026-01-02T07:29:27.565940', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('硅铁2612 (SF2612)', 'SF2612', '期货合约 SF2612 的交易建议。

品种代码: SF
当前价格: 7110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6754.50, 7110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.568662', '2026-01-02T07:29:27.568226', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('WH主力合约 (WH503)', 'WH503', '期货合约 WH503 的交易建议。

品种代码: WH
当前价格: 3198.0
现货价格: 2616.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:23:44.609831', '2026-01-02T06:23:44.609443', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PM主力合约 (PM503)', 'PM503', '期货合约 PM503 的交易建议。

品种代码: PM
当前价格: 3122.0
现货价格: 2616.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T06:23:44.611528', '2026-01-02T06:23:44.611166', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2603 (SM2603)', 'SM2603', '期货合约 SM2603 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.572259', '2026-01-02T07:29:27.571995', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2605 (SM2605)', 'SM2605', '期货合约 SM2605 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.574132', '2026-01-02T07:29:27.573751', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2607 (SM2607)', 'SM2607', '期货合约 SM2607 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.576084', '2026-01-02T07:29:27.575507', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2609 (SM2609)', 'SM2609', '期货合约 SM2609 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.579581', '2026-01-02T07:29:27.579038', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2611 (SM2611)', 'SM2611', '期货合约 SM2611 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.582102', '2026-01-02T07:29:27.581280', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2612 (SM2612)', 'SM2612', '期货合约 SM2612 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.584995', '2026-01-02T07:29:27.584499', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2601', 'CY2601', '期货合约 CY2601 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.588209', '2026-01-02T07:29:27.587628', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2603', 'CY2603', '期货合约 CY2603 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.590829', '2026-01-02T07:29:27.590238', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2605', 'CY2605', '期货合约 CY2605 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.593886', '2026-01-02T07:29:27.592952', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2607', 'CY2607', '期货合约 CY2607 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.597128', '2026-01-02T07:29:27.596610', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2609', 'CY2609', '期货合约 CY2609 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.599977', '2026-01-02T07:29:27.599078', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2611', 'CY2611', '期货合约 CY2611 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.602313', '2026-01-02T07:29:27.601893', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('CY2612', 'CY2612', '期货合约 CY2612 的交易建议。

品种代码: CY
当前价格: 21265.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 20201.75, 21265.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.606866', '2026-01-02T07:29:27.606265', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2601 (UR2601)', 'UR2601', '期货合约 UR2601 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.609394', '2026-01-02T07:29:27.608948', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2603 (UR2603)', 'UR2603', '期货合约 UR2603 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.615914', '2026-01-02T07:29:27.611272', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2605 (UR2605)', 'UR2605', '期货合约 UR2605 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.619228', '2026-01-02T07:29:27.618784', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2607 (UR2607)', 'UR2607', '期货合约 UR2607 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.621362', '2026-01-02T07:29:27.620892', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2609 (UR2609)', 'UR2609', '期货合约 UR2609 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.624872', '2026-01-02T07:29:27.623167', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2611 (UR2611)', 'UR2611', '期货合约 UR2611 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.628442', '2026-01-02T07:29:27.627741', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('尿素2612 (UR2612)', 'UR2612', '期货合约 UR2612 的交易建议。

品种代码: UR
当前价格: 2052.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 1949.40, 2052.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.631872', '2026-01-02T07:29:27.630855', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2601 (SA2601)', 'SA2601', '期货合约 SA2601 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.635129', '2026-01-02T07:29:27.634456', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锰硅2601 (SM2601)', 'SM2601', '期货合约 SM2601 的交易建议。

品种代码: SM
当前价格: 7808.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7417.60, 7808.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.570515', '2026-01-02T07:29:27.570123', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2603 (SA2603)', 'SA2603', '期货合约 SA2603 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.639165', '2026-01-02T07:29:27.638724', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2605 (SA2605)', 'SA2605', '期货合约 SA2605 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.642441', '2026-01-02T07:29:27.641929', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2609 (SA2609)', 'SA2609', '期货合约 SA2609 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.649710', '2026-01-02T07:29:27.648669', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2611 (SA2611)', 'SA2611', '期货合约 SA2611 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.652453', '2026-01-02T07:29:27.651781', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2612 (SA2612)', 'SA2612', '期货合约 SA2612 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.655989', '2026-01-02T07:29:27.655376', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2601 (PF2601)', 'PF2601', '期货合约 PF2601 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.658626', '2026-01-02T07:29:27.657957', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2603 (PF2603)', 'PF2603', '期货合约 PF2603 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.661181', '2026-01-02T07:29:27.660699', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2605 (PF2605)', 'PF2605', '期货合约 PF2605 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.667310', '2026-01-02T07:29:27.666839', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2607 (PF2607)', 'PF2607', '期货合约 PF2607 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.668835', '2026-01-02T07:29:27.668579', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2609 (PF2609)', 'PF2609', '期货合约 PF2609 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.671101', '2026-01-02T07:29:27.670692', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2611 (PF2611)', 'PF2611', '期货合约 PF2611 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.673049', '2026-01-02T07:29:27.672607', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('短纤2612 (PF2612)', 'PF2612', '期货合约 PF2612 的交易建议。

品种代码: PF
当前价格: 7386.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 7016.70, 7386.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.675096', '2026-01-02T07:29:27.674639', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2601', 'PX2601', '期货合约 PX2601 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.678041', '2026-01-02T07:29:27.677193', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2603', 'PX2603', '期货合约 PX2603 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.680700', '2026-01-02T07:29:27.680206', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2605', 'PX2605', '期货合约 PX2605 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.686804', '2026-01-02T07:29:27.686283', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2607', 'PX2607', '期货合约 PX2607 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.690905', '2026-01-02T07:29:27.690153', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2609', 'PX2609', '期货合约 PX2609 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.693477', '2026-01-02T07:29:27.692890', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2611', 'PX2611', '期货合约 PX2611 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.696435', '2026-01-02T07:29:27.696015', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('PX2612', 'PX2612', '期货合约 PX2612 的交易建议。

品种代码: PX
当前价格: 8486.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8061.70, 8486.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.698657', '2026-01-02T07:29:27.698217', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2601', 'SH2601', '期货合约 SH2601 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.700865', '2026-01-02T07:29:27.700322', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2603', 'SH2603', '期货合约 SH2603 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.705145', '2026-01-02T07:29:27.704557', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2605', 'SH2605', '期货合约 SH2605 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.708071', '2026-01-02T07:29:27.707443', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2607', 'SH2607', '期货合约 SH2607 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.710957', '2026-01-02T07:29:27.709837', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纯碱2607 (SA2607)', 'SA2607', '期货合约 SA2607 的交易建议。

品种代码: SA
当前价格: 2203.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2092.85, 2203.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.646401', '2026-01-02T07:29:27.644787', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2609', 'SH2609', '期货合约 SH2609 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.713395', '2026-01-02T07:29:27.712741', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2611', 'SH2611', '期货合约 SH2611 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.715306', '2026-01-02T07:29:27.714907', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2601 (CU2601)', 'CU2601', '期货合约 CU2601 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.719549', '2026-01-02T07:29:27.718765', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2603 (CU2603)', 'CU2603', '期货合约 CU2603 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.721886', '2026-01-02T07:29:27.721302', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2605 (CU2605)', 'CU2605', '期货合约 CU2605 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.723768', '2026-01-02T07:29:27.723415', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2607 (CU2607)', 'CU2607', '期货合约 CU2607 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.726123', '2026-01-02T07:29:27.725644', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2609 (CU2609)', 'CU2609', '期货合约 CU2609 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.730934', '2026-01-02T07:29:27.730367', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2611 (CU2611)', 'CU2611', '期货合约 CU2611 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.733445', '2026-01-02T07:29:27.732808', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2612 (CU2612)', 'CU2612', '期货合约 CU2612 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.737417', '2026-01-02T07:29:27.736858', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2601 (AL2601)', 'AL2601', '期货合约 AL2601 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.740011', '2026-01-02T07:29:27.739420', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2603 (AL2603)', 'AL2603', '期货合约 AL2603 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.742549', '2026-01-02T07:29:27.742085', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2605 (AL2605)', 'AL2605', '期货合约 AL2605 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.747140', '2026-01-02T07:29:27.746656', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2607 (AL2607)', 'AL2607', '期货合约 AL2607 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.749415', '2026-01-02T07:29:27.748879', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2609 (AL2609)', 'AL2609', '期货合约 AL2609 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.751677', '2026-01-02T07:29:27.751219', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2611 (AL2611)', 'AL2611', '期货合约 AL2611 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.755501', '2026-01-02T07:29:27.754707', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铝2612 (AL2612)', 'AL2612', '期货合约 AL2612 的交易建议。

品种代码: AL
当前价格: 20605.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 19574.75, 20605.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.758650', '2026-01-02T07:29:27.757891', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2601 (ZN2601)', 'ZN2601', '期货合约 ZN2601 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.761056', '2026-01-02T07:29:27.760594', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2603 (ZN2603)', 'ZN2603', '期货合约 ZN2603 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.764159', '2026-01-02T07:29:27.763597', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2605 (ZN2605)', 'ZN2605', '期货合约 ZN2605 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.769683', '2026-01-02T07:29:27.767666', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2607 (ZN2607)', 'ZN2607', '期货合约 ZN2607 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.775325', '2026-01-02T07:29:27.774753', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2609 (ZN2609)', 'ZN2609', '期货合约 ZN2609 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.778705', '2026-01-02T07:29:27.777312', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2611 (ZN2611)', 'ZN2611', '期货合约 ZN2611 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.781111', '2026-01-02T07:29:27.780618', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锌2612 (ZN2612)', 'ZN2612', '期货合约 ZN2612 的交易建议。

品种代码: ZN
当前价格: 23370.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 22201.50, 23370.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.783979', '2026-01-02T07:29:27.783545', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('SH2612', 'SH2612', '期货合约 SH2612 的交易建议。

品种代码: SH
当前价格: 2672.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2538.40, 2672.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.717332', '2026-01-02T07:29:27.716952', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2601 (PB2601)', 'PB2601', '期货合约 PB2601 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.790323', '2026-01-02T07:29:27.785540', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2603 (PB2603)', 'PB2603', '期货合约 PB2603 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.793173', '2026-01-02T07:29:27.792780', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2607 (PB2607)', 'PB2607', '期货合约 PB2607 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.797081', '2026-01-02T07:29:27.796714', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2609 (PB2609)', 'PB2609', '期货合约 PB2609 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.799446', '2026-01-02T07:29:27.799011', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2611 (PB2611)', 'PB2611', '期货合约 PB2611 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.801426', '2026-01-02T07:29:27.800852', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2612 (PB2612)', 'PB2612', '期货合约 PB2612 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.803335', '2026-01-02T07:29:27.802962', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2601 (NI2601)', 'NI2601', '期货合约 NI2601 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.805528', '2026-01-02T07:29:27.804865', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2603 (NI2603)', 'NI2603', '期货合约 NI2603 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.807129', '2026-01-02T07:29:27.806846', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2605 (NI2605)', 'NI2605', '期货合约 NI2605 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.808827', '2026-01-02T07:29:27.808474', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2607 (NI2607)', 'NI2607', '期货合约 NI2607 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.811065', '2026-01-02T07:29:27.810473', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2609 (NI2609)', 'NI2609', '期货合约 NI2609 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.814143', '2026-01-02T07:29:27.813705', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2611 (NI2611)', 'NI2611', '期货合约 NI2611 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.817364', '2026-01-02T07:29:27.816895', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2612 (NI2612)', 'NI2612', '期货合约 NI2612 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.819511', '2026-01-02T07:29:27.819059', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2601 (SN2601)', 'SN2601', '期货合约 SN2601 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.824039', '2026-01-02T07:29:27.823466', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2603 (SN2603)', 'SN2603', '期货合约 SN2603 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.827158', '2026-01-02T07:29:27.826753', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2605 (SN2605)', 'SN2605', '期货合约 SN2605 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.828949', '2026-01-02T07:29:27.828651', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2607 (SN2607)', 'SN2607', '期货合约 SN2607 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.830685', '2026-01-02T07:29:27.830248', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2609 (SN2609)', 'SN2609', '期货合约 SN2609 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.832243', '2026-01-02T07:29:27.831986', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2611 (SN2611)', 'SN2611', '期货合约 SN2611 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.833624', '2026-01-02T07:29:27.833232', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('锡2612 (SN2612)', 'SN2612', '期货合约 SN2612 的交易建议。

品种代码: SN
当前价格: 261360.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 248292.00, 261360.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.835747', '2026-01-02T07:29:27.835345', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2601 (AU2601)', 'AU2601', '期货合约 AU2601 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.837513', '2026-01-02T07:29:27.837085', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2603 (AU2603)', 'AU2603', '期货合约 AU2603 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.839265', '2026-01-02T07:29:27.838882', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2605 (AU2605)', 'AU2605', '期货合约 AU2605 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.841177', '2026-01-02T07:29:27.840733', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铅2605 (PB2605)', 'PB2605', '期货合约 PB2605 的交易建议。

品种代码: PB
当前价格: 17330.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16463.50, 17330.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.795187', '2026-01-02T07:29:27.794798', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2607 (AU2607)', 'AU2607', '期货合约 AU2607 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.843122', '2026-01-02T07:29:27.842775', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2609 (AU2609)', 'AU2609', '期货合约 AU2609 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.846425', '2026-01-02T07:29:27.845932', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2611 (AU2611)', 'AU2611', '期货合约 AU2611 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.848244', '2026-01-02T07:29:27.847908', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2612 (AU2612)', 'AU2612', '期货合约 AU2612 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.851698', '2026-01-02T07:29:27.851225', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2601 (AG2601)', 'AG2601', '期货合约 AG2601 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.855115', '2026-01-02T07:29:27.854546', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2603 (AG2603)', 'AG2603', '期货合约 AG2603 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.858319', '2026-01-02T07:29:27.857623', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2605 (AG2605)', 'AG2605', '期货合约 AG2605 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.860893', '2026-01-02T07:29:27.860388', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2609 (AG2609)', 'AG2609', '期货合约 AG2609 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.867874', '2026-01-02T07:29:27.867070', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2611 (AG2611)', 'AG2611', '期货合约 AG2611 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.871156', '2026-01-02T07:29:27.870659', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2612 (AG2612)', 'AG2612', '期货合约 AG2612 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.873235', '2026-01-02T07:29:27.872843', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2601 (RB2601)', 'RB2601', '期货合约 RB2601 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.875399', '2026-01-02T07:29:27.875015', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2603 (RB2603)', 'RB2603', '期货合约 RB2603 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.878062', '2026-01-02T07:29:27.877156', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2605 (RB2605)', 'RB2605', '期货合约 RB2605 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.881307', '2026-01-02T07:29:27.880868', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2607 (RB2607)', 'RB2607', '期货合约 RB2607 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.883804', '2026-01-02T07:29:27.883362', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2609 (RB2609)', 'RB2609', '期货合约 RB2609 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.888581', '2026-01-02T07:29:27.885974', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2611 (RB2611)', 'RB2611', '期货合约 RB2611 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.891318', '2026-01-02T07:29:27.890621', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('螺纹钢2612 (RB2612)', 'RB2612', '期货合约 RB2612 的交易建议。

品种代码: RB
当前价格: 3670.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3486.50, 3670.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.893018', '2026-01-02T07:29:27.892700', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2603 (WR2603)', 'WR2603', '期货合约 WR2603 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.896228', '2026-01-02T07:29:27.895967', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2605 (WR2605)', 'WR2605', '期货合约 WR2605 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.897766', '2026-01-02T07:29:27.897446', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2607 (WR2607)', 'WR2607', '期货合约 WR2607 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.899192', '2026-01-02T07:29:27.898903', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2609 (WR2609)', 'WR2609', '期货合约 WR2609 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.900474', '2026-01-02T07:29:27.900189', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2611 (WR2611)', 'WR2611', '期货合约 WR2611 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.902147', '2026-01-02T07:29:27.901867', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2612 (WR2612)', 'WR2612', '期货合约 WR2612 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.903528', '2026-01-02T07:29:27.903264', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('线材2601 (WR2601)', 'WR2601', '期货合约 WR2601 的交易建议。

品种代码: WR
当前价格: 3615.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3434.25, 3615.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.894678', '2026-01-02T07:29:27.894282', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2601 (HC2601)', 'HC2601', '期货合约 HC2601 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.907796', '2026-01-02T07:29:27.907202', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2603 (HC2603)', 'HC2603', '期货合约 HC2603 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.912092', '2026-01-02T07:29:27.911552', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2605 (HC2605)', 'HC2605', '期货合约 HC2605 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.915356', '2026-01-02T07:29:27.914894', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2607 (HC2607)', 'HC2607', '期货合约 HC2607 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.918365', '2026-01-02T07:29:27.917815', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2609 (HC2609)', 'HC2609', '期货合约 HC2609 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.927040', '2026-01-02T07:29:27.926567', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2612 (HC2612)', 'HC2612', '期货合约 HC2612 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.930393', '2026-01-02T07:29:27.930075', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2601 (FU2601)', 'FU2601', '期货合约 FU2601 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.932155', '2026-01-02T07:29:27.931837', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2603 (FU2603)', 'FU2603', '期货合约 FU2603 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.933646', '2026-01-02T07:29:27.933343', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2605 (FU2605)', 'FU2605', '期货合约 FU2605 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.935097', '2026-01-02T07:29:27.934810', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2607 (FU2607)', 'FU2607', '期货合约 FU2607 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.937009', '2026-01-02T07:29:27.936554', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2609 (FU2609)', 'FU2609', '期货合约 FU2609 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.938780', '2026-01-02T07:29:27.938460', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2611 (FU2611)', 'FU2611', '期货合约 FU2611 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.940398', '2026-01-02T07:29:27.940093', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('燃料油2612 (FU2612)', 'FU2612', '期货合约 FU2612 的交易建议。

品种代码: FU
当前价格: 3507.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3331.65, 3507.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.941931', '2026-01-02T07:29:27.941638', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2601 (BU2601)', 'BU2601', '期货合约 BU2601 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.943778', '2026-01-02T07:29:27.943359', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2605 (BU2605)', 'BU2605', '期货合约 BU2605 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.946785', '2026-01-02T07:29:27.946363', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2607 (BU2607)', 'BU2607', '期货合约 BU2607 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.948759', '2026-01-02T07:29:27.948368', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2609 (BU2609)', 'BU2609', '期货合约 BU2609 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.950883', '2026-01-02T07:29:27.950511', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2611 (BU2611)', 'BU2611', '期货合约 BU2611 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.953681', '2026-01-02T07:29:27.952487', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('沥青2612 (BU2612)', 'BU2612', '期货合约 BU2612 的交易建议。

品种代码: BU
当前价格: 3778.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3589.10, 3778.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.956063', '2026-01-02T07:29:27.955425', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2601 (RU2601)', 'RU2601', '期货合约 RU2601 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.957876', '2026-01-02T07:29:27.957499', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2603 (RU2603)', 'RU2603', '期货合约 RU2603 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.959707', '2026-01-02T07:29:27.959369', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2605 (RU2605)', 'RU2605', '期货合约 RU2605 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.962088', '2026-01-02T07:29:27.961673', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2607 (RU2607)', 'RU2607', '期货合约 RU2607 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.964065', '2026-01-02T07:29:27.963688', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2607 (AG2607)', 'AG2607', '期货合约 AG2607 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.864837', '2026-01-02T07:29:27.864155', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2609 (RU2609)', 'RU2609', '期货合约 RU2609 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.967050', '2026-01-02T07:29:27.965668', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2611 (RU2611)', 'RU2611', '期货合约 RU2611 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.969264', '2026-01-02T07:29:27.968777', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2605 (SS2605)', 'SS2605', '期货合约 SS2605 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.002874', '2026-01-02T07:29:28.002602', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2611 (SS2611)', 'SS2611', '期货合约 SS2611 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.007654', '2026-01-02T07:29:28.007377', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2612 (SS2612)', 'SS2612', '期货合约 SS2612 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.008938', '2026-01-02T07:29:28.008691', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2601 (BR2601)', 'BR2601', '期货合约 BR2601 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.010468', '2026-01-02T07:29:28.010152', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2603 (BR2603)', 'BR2603', '期货合约 BR2603 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.011942', '2026-01-02T07:29:28.011669', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2605 (BR2605)', 'BR2605', '期货合约 BR2605 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.013392', '2026-01-02T07:29:28.013131', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2607 (BR2607)', 'BR2607', '期货合约 BR2607 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.014688', '2026-01-02T07:29:28.014327', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2609 (BR2609)', 'BR2609', '期货合约 BR2609 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.016136', '2026-01-02T07:29:28.015875', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2611 (BR2611)', 'BR2611', '期货合约 BR2611 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.017397', '2026-01-02T07:29:28.017140', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('丁二烯橡胶2612 (BR2612)', 'BR2612', '期货合约 BR2612 的交易建议。

品种代码: BR
当前价格: 13135.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 12478.25, 13135.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.018704', '2026-01-02T07:29:28.018415', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2601 (SI2601)', 'SI2601', '期货合约 SI2601 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.020047', '2026-01-02T07:29:28.019799', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2603 (SI2603)', 'SI2603', '期货合约 SI2603 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.021240', '2026-01-02T07:29:28.021002', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2605 (SI2605)', 'SI2605', '期货合约 SI2605 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.022610', '2026-01-02T07:29:28.022316', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白糖2603 (SR2603)', 'SR2603', '期货合约 SR2603 的交易建议。

品种代码: SR
当前价格: 6161.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 5852.95, 6161.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.409486', '2026-01-02T07:29:27.409015', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('热轧卷板2611 (HC2611)', 'HC2611', '期货合约 HC2611 的交易建议。

品种代码: HC
当前价格: 3818.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3627.10, 3818.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.928807', '2026-01-02T07:29:27.928469', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2607 (SI2607)', 'SI2607', '期货合约 SI2607 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.023956', '2026-01-02T07:29:28.023705', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2609 (SI2609)', 'SI2609', '期货合约 SI2609 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.025309', '2026-01-02T07:29:28.025020', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2611 (SI2611)', 'SI2611', '期货合约 SI2611 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.026496', '2026-01-02T07:29:28.026249', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('工业硅2612 (SI2612)', 'SI2612', '期货合约 SI2612 的交易建议。

品种代码: SI
当前价格: 12045.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 11442.75, 12045.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.033893', '2026-01-02T07:29:28.033366', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2601 (LC2601)', 'LC2601', '期货合约 LC2601 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.036313', '2026-01-02T07:29:28.036001', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2603 (LC2603)', 'LC2603', '期货合约 LC2603 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.037785', '2026-01-02T07:29:28.037513', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('橡胶2612 (RU2612)', 'RU2612', '期货合约 RU2612 的交易建议。

品种代码: RU
当前价格: 14150.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13442.50, 14150.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.973650', '2026-01-02T07:29:27.973032', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2601 (SP2601)', 'SP2601', '期货合约 SP2601 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.975891', '2026-01-02T07:29:27.975408', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2603 (SP2603)', 'SP2603', '期货合约 SP2603 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.979391', '2026-01-02T07:29:27.978906', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2605 (SP2605)', 'SP2605', '期货合约 SP2605 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.982682', '2026-01-02T07:29:27.982167', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2607 (SP2607)', 'SP2607', '期货合约 SP2607 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.984192', '2026-01-02T07:29:27.983916', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2609 (SP2609)', 'SP2609', '期货合约 SP2609 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.985768', '2026-01-02T07:29:27.985337', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2611 (SP2611)', 'SP2611', '期货合约 SP2611 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.987777', '2026-01-02T07:29:27.987156', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('纸浆2612 (SP2612)', 'SP2612', '期货合约 SP2612 的交易建议。

品种代码: SP
当前价格: 6398.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6078.10, 6398.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.990490', '2026-01-02T07:29:27.990032', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2609 (PG2609)', 'PG2609', '期货合约 PG2609 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.338766', '2026-01-02T07:29:27.338492', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2611 (PG2611)', 'PG2611', '期货合约 PG2611 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.340052', '2026-01-02T07:29:27.339792', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2612 (PG2612)', 'PG2612', '期货合约 PG2612 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.341541', '2026-01-02T07:29:27.341301', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2601 (LH2601)', 'LH2601', '期货合约 LH2601 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.343105', '2026-01-02T07:29:27.342742', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2603 (LH2603)', 'LH2603', '期货合约 LH2603 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.344625', '2026-01-02T07:29:27.344330', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2605 (LH2605)', 'LH2605', '期货合约 LH2605 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.346839', '2026-01-02T07:29:27.346254', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2607 (LH2607)', 'LH2607', '期货合约 LH2607 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.348816', '2026-01-02T07:29:27.348445', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2609 (LH2609)', 'LH2609', '期货合约 LH2609 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.350710', '2026-01-02T07:29:27.350318', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2611 (LH2611)', 'LH2611', '期货合约 LH2611 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.353919', '2026-01-02T07:29:27.352814', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('生猪2612 (LH2612)', 'LH2612', '期货合约 LH2612 的交易建议。

品种代码: LH
当前价格: 17375.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 16506.25, 17375.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.356357', '2026-01-02T07:29:27.355975', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2601 (WH2601)', 'WH2601', '期货合约 WH2601 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.359226', '2026-01-02T07:29:27.358516', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2603 (A2603)', 'A2603', '期货合约 A2603 的交易建议。

品种代码: A
当前价格: 5098.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4843.10, 5098.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.081628', '2026-01-02T07:29:27.081128', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2605 (A2605)', 'A2605', '期货合约 A2605 的交易建议。

品种代码: A
当前价格: 5110.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4854.50, 5110.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.085107', '2026-01-02T07:29:27.084665', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2607 (A2607)', 'A2607', '期货合约 A2607 的交易建议。

品种代码: A
当前价格: 5068.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4814.60, 5068.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.090621', '2026-01-02T07:29:27.089986', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2609 (A2609)', 'A2609', '期货合约 A2609 的交易建议。

品种代码: A
当前价格: 5010.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4759.50, 5010.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.093503', '2026-01-02T07:29:27.093075', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('强麦2612 (WH2612)', 'WH2612', '期货合约 WH2612 的交易建议。

品种代码: WH
当前价格: 3198.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3038.10, 3198.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.373229', '2026-01-02T07:29:27.372816', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2601 (PM2601)', 'PM2601', '期货合约 PM2601 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.375100', '2026-01-02T07:29:27.374709', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('普麦2612 (PM2612)', 'PM2612', '期货合约 PM2612 的交易建议。

品种代码: PM
当前价格: 3122.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 2965.90, 3122.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.389691', '2026-01-02T07:29:27.389364', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2601 (CF2601)', 'CF2601', '期货合约 CF2601 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.391422', '2026-01-02T07:29:27.391011', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('棉花2603 (CF2603)', 'CF2603', '期货合约 CF2603 的交易建议。

品种代码: CF
当前价格: 15700.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 14915.00, 15700.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.393476', '2026-01-02T07:29:27.393145', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2605 (LC2605)', 'LC2605', '期货合约 LC2605 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.039432', '2026-01-02T07:29:28.039077', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2607 (LC2607)', 'LC2607', '期货合约 LC2607 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.040889', '2026-01-02T07:29:28.040627', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2609 (LC2609)', 'LC2609', '期货合约 LC2609 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.042116', '2026-01-02T07:29:28.041878', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2611 (LC2611)', 'LC2611', '期货合约 LC2611 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.043389', '2026-01-02T07:29:28.043134', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('碳酸锂2612 (LC2612)', 'LC2612', '期货合约 LC2612 的交易建议。

品种代码: LC
当前价格: 113250.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 107587.50, 113250.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.044658', '2026-01-02T07:29:28.044386', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2602', 'AG2602', '期货合约 AG2602 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:38.143363', '2026-01-02T08:49:34.525835', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('白银2606', 'AG2606', '期货合约 AG2606 的交易建议。

品种代码: AG
当前价格: 7053.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 6700.35, 7053.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:40.540877', '2026-01-02T08:49:38.149256', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('黄金2606', 'AU2606', '期货合约 AU2606 的交易建议。

品种代码: AU
当前价格: 552.8

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 525.16, 552.80, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:43.419678', '2026-01-02T08:49:40.543427', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('铜2602', 'CU2602', '期货合约 CU2602 的交易建议。

品种代码: CU
当前价格: 81770.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 77681.50, 81770.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:45.853799', '2026-01-02T08:49:43.421342', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('镍2602', 'NI2602', '期货合约 NI2602 的交易建议。

品种代码: NI
当前价格: 143950.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 136752.50, 143950.00, 'buy', '待管理员编辑建议', 2, 1, '2026-01-02T08:49:48.257745', '2026-01-02T08:49:45.857063', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2611 (EG2611)', 'EG2611', '期货合约 EG2611 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.312672', '2026-01-02T07:29:27.312186', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('乙二醇2612 (EG2612)', 'EG2612', '期货合约 EG2612 的交易建议。

品种代码: EG
当前价格: 4453.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4230.35, 4453.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.315117', '2026-01-02T07:29:27.314632', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2601 (EB2601)', 'EB2601', '期货合约 EB2601 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.317695', '2026-01-02T07:29:27.317207', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2603 (EB2603)', 'EB2603', '期货合约 EB2603 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.324999', '2026-01-02T07:29:27.324593', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2605 (EB2605)', 'EB2605', '期货合约 EB2605 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.326510', '2026-01-02T07:29:27.326218', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2607 (EB2607)', 'EB2607', '期货合约 EB2607 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.327895', '2026-01-02T07:29:27.327635', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2609 (EB2609)', 'EB2609', '期货合约 EB2609 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.329171', '2026-01-02T07:29:27.328910', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2611 (EB2611)', 'EB2611', '期货合约 EB2611 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.330777', '2026-01-02T07:29:27.330494', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('苯乙烯2612 (EB2612)', 'EB2612', '期货合约 EB2612 的交易建议。

品种代码: EB
当前价格: 9384.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 8914.80, 9384.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.332064', '2026-01-02T07:29:27.331817', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2601 (PG2601)', 'PG2601', '期货合约 PG2601 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.333267', '2026-01-02T07:29:27.333010', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('液化石油气2603 (PG2603)', 'PG2603', '期货合约 PG2603 的交易建议。

品种代码: PG
当前价格: 4606.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4375.70, 4606.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.334553', '2026-01-02T07:29:27.334308', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2607 (SS2607)', 'SS2607', '期货合约 SS2607 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.004814', '2026-01-02T07:29:28.004508', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2609 (SS2609)', 'SS2609', '期货合约 SS2609 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.006238', '2026-01-02T07:29:28.005943', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2611 (A2611)', 'A2611', '期货合约 A2611 的交易建议。

品种代码: A
当前价格: 5032.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4780.40, 5032.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.096931', '2026-01-02T07:29:27.096316', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('豆一2612 (A2612)', 'A2612', '期货合约 A2612 的交易建议。

品种代码: A
当前价格: 5036.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 4784.20, 5036.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.104148', '2026-01-02T07:29:27.103605', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2601 (JD2601)', 'JD2601', '期货合约 JD2601 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.184314', '2026-01-02T07:29:27.183771', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2603 (JD2603)', 'JD2603', '期货合约 JD2603 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.187924', '2026-01-02T07:29:27.186426', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2605 (JD2605)', 'JD2605', '期货合约 JD2605 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.191732', '2026-01-02T07:29:27.191222', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2607 (JD2607)', 'JD2607', '期货合约 JD2607 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.196821', '2026-01-02T07:29:27.196166', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2609 (JD2609)', 'JD2609', '期货合约 JD2609 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.202870', '2026-01-02T07:29:27.199070', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('鸡蛋2611 (JD2611)', 'JD2611', '期货合约 JD2611 的交易建议。

品种代码: JD
当前价格: 3917.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 3721.15, 3917.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.209624', '2026-01-02T07:29:27.209183', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2601 (SS2601)', 'SS2601', '期货合约 SS2601 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:27.999164', '2026-01-02T07:29:27.998629', '2026-01-02T01:23:54.913024');
INSERT INTO posts (title, contract_code, content, stop_loss, current_price, direction, suggestion, author_id, status, publish_time, created_at, updated_at) VALUES ('不锈钢2603 (SS2603)', 'SS2603', '期货合约 SS2603 的交易建议。

品种代码: SS
当前价格: 14325.0

请管理员编辑此帖子的交易建议、止损价、止盈价等信息。', 13608.75, 14325.00, 'buy', '待管理员编辑建议', 5, 1, '2026-01-02T07:29:28.001168', '2026-01-02T07:29:28.000852', '2026-01-02T01:23:54.913024');
