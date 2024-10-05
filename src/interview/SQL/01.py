# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/4 11:12
    @File   : 01.py
    @Desc   :
"""

"""
表1：t_user 分区字段 dt yyyy-MM-dd 全量同步  hive表：dw_active.t_user
表结构：
  user          string   唯一主键
  name          string
  status        int     0-失效，,1-有效；
  country_id    int  与下文中 country 表 id 可做关联，获取 country_name
  created       string (2022-08-22 16:00:01)

----- 
表2：t_country 表 分区字段dt yyyy-MM-dd 全量同步  hive表：dw_active.t_country表
表结构
  id int;  国家id
  country_name string 国家名称
  status int;

-----
表3：t_login 表 分区字段dt yyyy-MM-dd 增量同步  hive表：dw_active.t_login
表结构
  user string
  state int     0-失效，,1-有效；
  platform int
  created string (2022-08-22 16:00:01)
  updated string (2022-08-22 16:00:01))

问题： （3 选 2 即可）
 1- 统计指定日期下的 近10天 用户登陆（一条记录为一次记录，不考虑去重）的国家 top10，请输出 日期、国家名称、访问次数；
  建议控制一下日期参数，实现任务可回溯、可无脑重试
  
  SELECT
    t_country.id as c_id,
    t_country.country_name,
    count(t_login.id) as l_id
FROM
    t_user,
    t_login,
    t_country 
WHERE
    t_user.id = t_login.user
    AND t_user.country_id = t_country.id    
    AND t_login.updated > "2022-08-22 16:00:01"
    GROUP BY t_country.id
    ORDER BY l_id DESC
    limit 10;

 2- 在 t_user 表保证 user 唯一的情况下，统计出 t_user 表中 status=1 的用户数量；
    select count(*) from t_user where status=1
 3- 统计出 指定日期下 近 30填，登录国家的用户数，按照登录人数 降序排列；
    SELECT
    t_country.id as c_id,
    COUNT(distinct(t_user.id)) as u_id
FROM
    t_user,
    t_login,
    t_country 
WHERE
    t_user.id = t_login.user
    AND t_user.country_id = t_country.id    
    AND t_login.updated > "2022-08-22 16:00:01"
    GROUP BY t_country.id
    ORDER BY u_id desc
"""


















