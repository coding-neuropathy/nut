4. 
3. SKU, Order ,CartItem, OrderItem inherted from BaseModel
2. move BaseModel to independent file
1. remove SKU, Order, CartItem dependency from core.models

=============

7. gk manage order list 
6. tag page update
--------
5. paid order reduce sku stock 
4. wx prepay id api
3. payment log update
2. entity qrcode add ?from=qrcode
1. add discount property  into SKU model 


action : 
    1. drop payment log table 
    
        DROP TABLE `core`.`payment_paymentlog`;
        
    2. syncdb 

    
    3.  add discount field 
    ALTER TABLE `core`.`order_sku` 
    ADD COLUMN `discount` FLOAT NOT NULL DEFAULT 1 AFTER `status`;

       已经执行



=============================
# merged to master 2016 8-15
=============================

2. update design week api
1. update common_shop_link for shop_shop


=======================
# merged to master 2016 8-12
=======================


3. design week api 
2. fix seller add entity form bug 
1. fix seller sku add and edit bug

=======================
# merged to master 2016 8-11
=======================

4. article feed count to 20 
3. remove pic in header 
2. order  : seller sku/entity management 
1. hot article tags (not top article tags)

 
See : 

TagsManager.hot_article_tags()

Action : 
    1. syncdb 
    
    --- only run this if you already synced order models -----
    2. if you already have order_*** table created 
       run following 
       
        ALTER TABLE `core`.`order_order` 
        ADD COLUMN `created_datetime` DATETIME NOT NULL AFTER `shipping_to_id`,
        ADD COLUMN `updated_datetime` DATETIME NOT NULL AFTER `created_datetime`;


=======================
# merged to master 2016 8-8
=======================

4. article mobile page bug(user link) fix 
3. remove hot enity ajax loading and add cache 
2. random recommend user 
1. add auth_token function for rest-api

action :
   need sync db 
   add  authtoken_token from rest-framework
   
    

=======================
# merged to master 2016 7-29
=======================

5. web bug fix (top bar element margin, article remark mobile display , etc)
4. index page hot entity use ajax 
3. push notification formal send 
2. web scroll bug fix 
1. article remark mobile 


action : 

ALTER TABLE `core`.`notifications_dailypush` 
CHANGE COLUMN `send_time` `send_time` DATETIME NULL ;


=====================
5.  management editor workload data report 
4.  management add entity - update
3.  index page category icon
2.  index page search header 
1.  mobile article page image display bug fix 

=======================
# merged to master 2016 7-18
=======================
3. update tag article template 
2. add short_digest to Article model ,and handle cache
1. translation update 

action : need restart server 
         translation update 

=======================
# merged to master 2016 7-14
=======================

5. index page update 
4. bran page bug fix 
3. tag page bug fix 
2. optimize index query count , reduce 40 query 
1. fix index banner size , to 750 px 

action: 

  need restart server , translation update
  

=======================
# merged to master 2016 7-7
=======================
7. mng - operation report 
6. web - index page refactor 
5. mng - editor work report update,sorting 
4. web -fix notification pic size bug 
3. web -fix tag page entity display bug 
2. web - display entity's brand link in detail page , if its published 
1. web -fix selection list page , time para cause 500 error 


=======================
# merged to master 2016 7-1 
=======================

1. fix index page bug 

=======================
# merged to master 2016 6-30 
=======================

3. editor work report (alpha)
2. index page 
1. add note to tag entity list  

=======================
# merged to master 2016 6-27
=======================


3. mng  tag page search function 
2. fix message page refresh bug 
1. add article enter selection time  for solr index 

=======================
# merged to master 2016 6-25
=======================

3. tag page raw list link , show buy link
2. tag page add raw list link , only for staff user 
1. fix web user add entity bug 
=======================
# merged to master 2016 6-24
=======================

6.  other add new index field for article enter selection time 
5.  mng - article list seperate rss author
          article author list sort bug fix 
4.  mng - tag mng , publish , raw data page 
3.  web - notification  loading pic 
2.  web - article  detail page  update, limit new remark rate , in view. 
1.  web - 发现页－推荐用户 - 滚动 - LQ

action: 

ALTER TABLE `core`.`tag_tags` 
ADD COLUMN `isPubishedEntityTag` TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE `core`.`tag_tags` ADD COLUMN `description` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL;
=======================
# merged to master 2016 6-16
=======================

5. mng - like entity report 
4. web - new article detail page 
3. web - top menu notification 
2. web - in removed entity's detail page , add search button
1. web - sub category sort buy like (bug fix )

action : 
  ALTER TABLE `core`.`shop_shop` 
ADD COLUMN `tb_shop_id` VARCHAR(64) NULL DEFAULT NULL AFTER `shop_type`;


=======================
# merged to master 2016 6-2
=======================

4.  good store update 
3.  broadcast  push management , test send
2.  jpush notification , add android push 
1.  add a Entity property :  is_pubed_selection 

Action : 
    1. add solr/haystack Entity index field (property) 
         1.  is_pubed_selection
         2.  enter_selection_time  
       
    2. need sync db 
        add DailyPush model    
        
    3. fix field encoding , if needed 
        ALTER T
        ABLE `core`.`notifications_dailypush` 
CHANGE COLUMN `push_text` `push_text` VARCHAR(64) CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci' NOT NULL ;
     
####  for  entity buylink update use 

ALTER TABLE `core`.`core_buy_link` 
ADD COLUMN `last_update` DATETIME NOT NULL DEFAULT '2013-12-01T00:00:00.000' AFTER `foreign_price`;

=======================
# merged to master 2016 5-26
=======================


8.  web - brand page update --along
7.  web - user add entity tmall price fix --along 
6.  web - fix event page bug  -- lq
5.  mng - selection entity batch new/freeze/remove --lq
4.  api - app banner api switch    -- anchen 
3.  web  -good-store optimize  -- lq
2.  web  -update recommend user discover page display count to 10 -an 
1.  other - price qr code update  -- anchen



git =======================
# merged to master 2016 5-23
=======================

5. update google analysis code 
4. web -pop up store top banner -- lq
3. api - article.digest filter blank characters  
2. other - price tag html 
1. mng - editor can  access brand list page and manage brand entity

=======================
# merged to master 2016 5-19
=======================

8. web - new article feed for editor selection article 
7. web - good store page update  -- lq , ac
6. web - entity detail , sold out entity add "去店铺" button
5. web - recommended user name and all recommended user  page    -- lq
4. mng - tmall price    -- along 
3. mng - add '积极用户' manage    --  along
2. backend - limit guoku generated email address , verify mail and change pass mail sending
1. web - hide baichuan title when load fail 

=======================
# merged to master 2016 5-12
=======================

5.  search result highlight -- jiaxin 
4.  site banner management (api will update at next monday, MNG first )  -- shuailong
3.  wechat robot  -- anchen 
2.  article page can not be zoom by user, mobile (bug fix) -- anchen
1.  limit manage entity create editor choice to 8 and self  -- anchen

#action need sync db 
    add  RobotDic model for wechat robot 
    
    
 may have been some text problem-   
after  syncdb on test server , on mng page 
following error appears 

 (1267, "Illegal mix of collations (latin1_swedish_ci,IMPLICIT) and (utf8mb4_general_ci,COERCIBLE) for operation '='")
 

ALTER TABLE `core`.`wechat_robotdic` 
CHANGE COLUMN `keyword` `keyword` VARCHAR(128) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL ,
CHANGE COLUMN `resp` `resp` VARCHAR(1024) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL ;


 
=======================
# merged to master 2016 5-9
=======================

5.  mng -  guoku editor/writer article list  -- anchen 
4.  article page not found to 404 page , for searching engine consideration -- anchen
3.  selection entity long pic css adjust , event entity pic vertical align  -- 罗倩
2.  editor user can use management , except user edit --anchen 
1.  add nick to core/model  -- 赵旭

=======================
# merged to master 2016 5-5
=======================

5. mng - entity list  - add editor frozen entity list 
4. mng - entity edit - add link to selection time edit

2. add source field to Article model (0 for local , 1 for weixin , 2 for rss)
   add origin_url  field  into the Article model  
   
1. block web user load entity request in 7 seconds

#action : 

origin_source is add by huanghuang and not documented !!
will not touch it . 

ALTER TABLE `core`.`core_article` 
ADD COLUMN `source` TINYINT(2) NULL DEFAULT 0 AFTER `origin_source`;

ALTER TABLE `core`.`core_article` 
ADD COLUMN `origin_url` VARCHAR(255) NULL DEFAULT NULL AFTER `source`;


MORE action 


=======================
# merged to master 2016 4-28
=======================


7. MNG - fix amazon book product can not get image bug -- along 
6. WEB - discover page , category slider   -- 罗倩
5. API - user dic  add nick field for shorten user nick name  -- 赵旭
3. MNG  - mng article , sortable  , by id and publish time  -- 赵旭
2. MNG  - brand mng update   - 安
1. move secret config into secret file   - 安


#ACTION 
none
    
    
    
    
=======================
# merged to master 2016 4-21
=======================

4. fix web group category page ajax refresh bug 
3. fix api entity guess category id fail 
2. add article mng edit author selection 
1. brand entity management  

##action

CREATE TABLE `core_entity_brand` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `entity_id` integer NOT NULL UNIQUE,
    `brand_id` integer NOT NULL,
    `brand_order` integer NOT NULL
)
;
ALTER TABLE `core_entity_brand` ADD CONSTRAINT `entity_id_refs_id_baee5e01` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);


IMPORTANT  !!  WHY SKIP the following: 

  when  syncdb 
  for  Entity_Brand model 
  
  when excute  syncdb in local , 
  encounter error :  cannot add foreign key constraint
                   
  done a lot test 
                              
  even defined model like this to avoid naming conflict   :
  
class Dog(BaseModel):
    cat = models.ForeignKey(Brand, related_name='ant')
    miao = models.IntegerField()    
                           
  still can not add brand_id constraint,
  the id column in core_brand table must has something wrong 
  
  so , for last resort  create table by hand instead.
 
  without the brand_id constraint , when add data to entity_brand 
  , database will not check if the brand_id in core_brand table 
  , these is not a problem for now .
  
                             
  pls pay attention 


=======================
# merged to master 2016 4-17
=======================

1. fix category  new_or_selection , sort bug ,
 
==================================
# merged to master 2016 4-14 
==================================

14.  API: discover page article , add digest 
13.  API:  filter removed user in activity/message 
12.  article craw report update 
11.  article mng edit , tag ,add parent category words for selection
10.  good store , new banner 
9.  API , FAN , following  list , category entity list , bug fix 
8.  optimize user like category list query , reduce 2000ms query time 
7.  article edit (web) no permission  REDIRECT to 403 page 
6.  article edit (mng) support chinese comma
5.  recommend user count up to 16 
4.  api article list page , add field 'digest' for short article digest
3.  fix category display int entity page header and description 
2.  new category detail page , 
    new subcategory page , 
    new subcategory list page        --zhaoxu , luoqian  
1.  discovery page  , category list  --zhaoxu , luoqian 

==================================
# merged to master 2016 4-7 
==================================

6. reset password page refactor  --zhaoxu, luoqian 
5. fix entity liker 500 bug (see bug discussion below) --anchen
4. brand page style update    -- luoqian 
3. hidden pink button when media widh< 768 -- luoqian 
2. baidu tracker selection page -- zuoning (not finished)
1. kaola margin link generate   -- shuailong 

##action 

##about entity liker page BUG 

for some row in table core_entity_like, 
    column 'user_id' has value , 
    which can not find in core_gkuser;


SELECT core_entity_like.* FROM core.core_entity_like where user_id not in ( select  id from core_gkuser)


temp solution :

    entity_liker_list.html  , skip those like entities;

final solution: 

    delete those entries in core_entity_like



==================================
# merged to master 2016 3 - 31
==================================

8. good_store update, seller index page update --luoqian, zhaoxu 
7. new cooperate static page         -- zuoning
6. crawl article report update       -- shuailong , zuoning 
5. fix poke multi post bug           -- zuoning 
4. reinstall baichuan recommend      -- An
3. kaola image get fix               -- shuailong 
2. bottom download bar for mobile access  -- Luoqian
1. fix mng brand state page bug           -- Luoqian

## action 

   有翻译更新  需要 
   ./manage.py compilemessages
   
   和重启SERVER 

==================================
# merged to master 2016 3 - 25
==================================

5. brand page (no entry)
4. user digged article page 
3. seller user page 
2. good store page update (no entry ) 
1. move article read query to slave  

#note
 
 如果出现锁表,家欣哥可以发导致锁表的SQL给我, 我再调整.
 

==================================
# merged to master 2016 3 - 20
==================================

2. article tag recommendation  
1. Entity add top note cache  , reduce 40 query per page 

==================================
# merged to master 2016 3 - 19
==================================
 
1.  remove baichuan rec for now 
0.  article tag editing (unfinished)
==================================
# merged to master 2016 3 - 17
==================================
6. GKUser.digs 实现方式 

5. good store page 
4. mng article creator choice method update
3. article dig count cache time 
2. brand mng list search 
1. add brand score for control recommend brand order 

## careful 
   测试服务器出现中文 store page banner title 不能提交的问题
   不一定要运行,生产服务器已经OK 
   
    ALTER TABLE `core`.`shop_storepagebanners` 
CHANGE COLUMN `banner_title` `banner_title` VARCHAR(128) CHARACTER SET 'utf8' COLLATE 'utf8_bin' NULL DEFAULT NULL ,
CHANGE COLUMN `banner_desc` `banner_desc` VARCHAR(128) CHARACTER SET 'utf8' COLLATE 'utf8_bin' NULL DEFAULT NULL ;

## need run sql 

ALTER TABLE `core`.`core_brand` 
ADD COLUMN `score` INT(32) NULL DEFAULT 0 AFTER `tmall_link`;


### add  a column  'score' on Brand model ,

    for fine control the brand order 

==================================
# merged to master 2016 3 - 10 
==================================

2. store page recommend mng
1. store page banner mng 
0. article dig js update

#action 

need syncdb 


=================================
# merged to master 2016 － 3 － 4
=================================


# remove fetch_article module.

### action

    ALTER TABLE `core`.`core_article` 
    CHANGE COLUMN `cleaned_title` `identity_code` VARCHAR(255) NULL     DEFAULT NULL COMMENT '' ;

===




5.  article hide weixin id when author don't have it 
4.  shop style and type choice update (management )
3.  show article dig message in message page 
2.  article dig 
1.  fix web message page bug (new selection)

=================================
# merged to master 2016 － 2 － 29
=================================


3.  authorized seller shop management
2.  api user article list bug fig 
1.  article writer follow button position 

#action 

ALTER TABLE `core`.`shop_shop` 
CHANGE COLUMN `shop_desc` `shop_desc` VARCHAR(511) CHARACTER SET 'utf8mb4' NULL ,
CHANGE COLUMN `shop_brands` `shop_brands` VARCHAR(255) CHARACTER SET 'utf8mb4' NULL ;

ALTER TABLE `core`.`shop_shop` 
ADD COLUMN `shop_style` INT(8) NULL DEFAULT 0 AFTER `shop_brands`,
ADD COLUMN `shop_type` INT(8) NULL DEFAULT 0 AFTER `shop_style`;



=================================
# merged to master 2016 － 2 － 25
=================================

4.  discover page , recommended user 
3.  authorized user profile add 3 field (points, is_recommended_user, rss_url)
2.  discover page add popular article 
1.  article page user info update
    article page add user follow

##action 

ALTER TABLE `core`.`core_authorized_user_profile` 
ADD COLUMN `points` INT(32) NOT NULL DEFAULT 0 AFTER `personal_domain_name`;

ALTER TABLE `core`.`core_authorized_user_profile` 
ADD COLUMN `is_recommended_user` TINYINT(1) NOT NULL DEFAULT 0 AFTER `points`;

ALTER TABLE `core`.`core_authorized_user_profile` 
ADD COLUMN `rss_url` VARCHAR(255) NULL AFTER `is_recommended_user`;

=================================
# merged to master 2016 － 2 － 22
=================================

5. remove 好店 导航入口
4. minor bug fix 
3. category detail page related article 
2. add entity share 
1.  update article share


=================================
# merged to master 2016 － 2 － 19
=================================

9. remove qrcodeService , use js render qrcode instead

------------------
8. fix entity detail image small for ali/taobao cdn bug
7. Qrcode service for share use (save file need more work , hidden )
6. share Entity (not finished / branch merged )
5. share article ( not finished/ branch not merged )
4. management : manage seller shops (not finished )
3. management : set user to seller (add 'Seller' group to user's group list)
2. fix seller page bug
1. header css adjust

##action:

need syncdb

###add shops_shop new model

notice : qrcodeService model removed

=================================
=================================
### merged to master 2016 － 2 － 5
=================================
=================================


4. 春节 h5 
3. new footer
2. show baichuan recommend products
1. fix  '//images....' replace bug caused by None img field
0.5  alicdn and taobaocdn image resize 

=================================
#merged to master 2016 － 2 － 2
=================================

2. disable like action for search result 
1. fix rss bug

=================================
# merged to master 2016 － 2 － 1
=================================

3. category entity list item style update
2. fix Article model created_datetime auto_add 
1. article writer bio update


=================================
# merged to master 2016 － 1 － 27
=================================

### fix can not create article error:

##action

    ALTER TABLE `core`.`core_article` DROP INDEX `cleaned_title_UNIQUE` ;


7. article mobile page css adjust 
6. add a cookie store for sogou spider use 
-----------------------
5. article mng list page change
4. article mng edit page change 
3. entity liker list and fan following list template fix 
2. download page url , without ending slash , access 
1. hide deleted user in user fan/following list 

##action 
 need sync db 
 
 
 need  manage.py compilemessages 
 need  restart server  (new translation items )
 
 
 ##action

    sudo pip install fake-factory

    ALTER TABLE `core`.`core_authorized_user_profile` 
    ADD COLUMN `weixin_openid` VARCHAR(255) NULL COMMENT '' AFTER `weibo_nick`;
   
    ALTER TABLE `core`.`core_article` 
    ADD COLUMN `cleaned_title` VARCHAR(255) NULL COMMENT '' AFTER `feed_read_count`,
    ADD UNIQUE INDEX `cleaned_title_UNIQUE` (`cleaned_title` ASC)  COMMENT '';
    

##2016-02-22 Fetch wixin articles

 



=================================
# merged to master 2016 － 1 － 21
=================================


5. minor fix 
    (pc article page add ga, xs screen article pic cross full screen)

4. add a field on authorized user profile 

3. Entity 's related Selection Article 

   Entity has a property: 
                selected_related_articles
   contains all Entity's related Selection_Article instance  (NOT Article!)
                published before called time

2. add tags_string  property for Article model
   
   Article.tags_string 
      : get Articles Tag joined into a string by ',' 
   
1. still hide baichuan recommend


##action

ALTER TABLE `core`.`core_authorized_user_profile` 
ADD COLUMN `personal_domain_name` VARCHAR(64) NULL DEFAULT NULL AFTER `weibo_nick`;



=================================
=================================
### merged to master 2016 － 1 － 18
=================================
=================================

5. use CBV for user list 
4. user list search
3. baichuan recommendation  (hide for now)
2. user set to author 
1. a bookmark for youzhan's taobao product adding , not for web 
   but put in doc anyway

##action  

need syncdb 


2016-1-13 start 

=================================
=================================
### merged to master 2016 － 1 － 12
=================================
=================================

6. add home link in store2015 page 
5. store2015 entity list display bug fix
4. freeze entity liker won't display bug fix
3. in guoku editor 
   a. if article's change is not saved , user can not leave page without passthrough a confirmation dialog;
   b. removeFormat button now working ok 
   c. after past html , the style in other content won't be removed
  
2. fix register page word error (Have an Account? )
1. fix user can not send verify mail , if user location is not in default list (app reged user)

###action 
### 翻译有更新
  需要  compilemessages
  需要重新启动 让翻译生效 

=================================
=================================
### merged to master 2016 － 1 － 8
=================================
=================================

3. fast click optimize for mobile browsers 
2. m.guoku.com store2015 page , weixin browser , entity click to app download 
1. fix store 2015 weibo share page pic bug

2016－1-8 start

=================================
=================================
### merged to master 2016 － 1 － 7
=================================
=================================

5. guoku assigned email , no verify , alert to change mail . 
4. store 2015 front
3. 搜索记录同时记录用户的ip和agent
2. 首页瀑布流
1. update redis key user_last_verify_time_id to user_last_verify_time:id

### 翻译有更新
  需要  compilemessages
  需要重新启动 让翻译生效 

### action

    ALTER TABLE `core`.`core_search_history` 
    ADD COLUMN `ip` VARCHAR(45) NULL COMMENT '' AFTER `search_time`,
    ADD COLUMN `agent` VARCHAR(255) NULL COMMENT '' AFTER `ip`;
    
    ALTER TABLE `core`.`core_search_history` 
    CHANGE COLUMN `key_words` `key_words` VARCHAR(255) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL COMMENT '' ;

    
1 ： 果库Top 100 淘宝卖家    
    
2015-12-30
===
    
---    
=================================
=================================
### merged to master 2015-12-28
=================================
=================================



4.  no more christmas logo
3.  fix management search paging bug
2.  seller web page 
1.  seller management update

=================================
=================================
### merged to master 2015-12-23
=================================
=================================

7. user page side bar (not user index page side bar) , 
    disable user article link if user do not have article (done)
     
6. user page, display user article when user has article 
    (currently only display when user can write) (done)
    
5. xs screen selection_entity page bg-color : #f8f8f8 （done）
4. display 2 entity in a row (done)
3. display all note on selection entity page.(done)


------  not finished  ---- 
2. friendly link , new style (NOT finished )
1. in wechat browser , if product is from taobao/tmall , 
    buy button jump to app download page (NOT finished)
----------------


1. add seller section management views and templates



### Action
1.  drop table : seller_seller_profile
2.  drop table : seller_seller_profile_related_articles   
3.  need Sync DB 


2015-12-20 

=================================
=================================
### merged to master 2015-12-17
=================================
=================================

2. fix event page selection entity css broken bug 
1. fix liker list page css broken bug 
  
#### Action
  * update django-sendcloud: 

        sudo pip install git+git://github.com/guoku/django-sendcloud@master
          
        
  * update db: 

        CREATE TABLE `core_sd_address_list` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `address` varchar(45) NOT NULL,
        `name` varchar(45) NOT NULL,
        `description` varchar(45) NOT NULL,
        `created` datetime NOT NULL,
        `members_count` integer NOT NULL
        );

INSERT INTO `core`.`core_sd_address_list` (`address`, `name`, `description`, `members_count`, `created`) VALUES ('gk_users_1@maillist.sendcloud.org', 'gk_users_1', 'gk_users_1', '11017', '2015-12-16 17:04:21');

####Changelog:

1. fix feed read counter bug


2. 首页瀑布流
1. update redis key user_last_verify_time_id to user_last_verify_time:id

-------

fix bug: category entities order by olike can't load more entity when screen scroll to bottom.

-------

1. 用户注册、激活、需改信息..时，对SendCloud的操作改为使用celery;
2. 动态获取和创建SendCloud地址列表;
3. 只有激活了的邮箱才会加入到sendcloud地址列表；
4. 开始着手写test，写了一些关于account和edm的。

-------

4.  minor bug fix 
3.  user liker app in entity detail page
3. event page, m.guoku.com, simple title (not finish)
2. add seller management files
1. add seller model 

### Action  
need syncdb  
for new seller table




=================================
=================================
### merged to master 2015-12-10
=================================
=================================


4.  minor display bug fix 
3.  user liker app in entity detail page / restful API 
2.  add analysis.guoku.com's tracking code 
1.  make sure this is no overflow in counter values.


### ACTION
ALTER TABLE `core`.`core_article` 
CHANGE COLUMN `read_count` `read_count` INT(32) UNSIGNED ZEROFILL NULL DEFAULT 0 ,
CHANGE COLUMN `feed_read_count` `feed_read_count` INT(32) UNSIGNED ZEROFILL NULL DEFAULT 0 ;





=================================
=================================
## merged to master 2015 - 12 - 3
=================================
=================================

5.修改edm收件地址列表，从测试列表改为正式列表。修改settings所以需要重启服务
4. article page weixin share url move to m.guoku.com 
3. user email verify functions 
2. user setting pages css refactor  
1. add some tests for tag(It's not enough). by judy 
 
==== 2015-12-03 ==== start 


## merged to master 2015 - 11 -30

5. FIX tag list page  paging function bug
4. event list page is now the default event link target
3. user likes page category filter 
2. user following/fans page refactor , add followee/follower recent likes 
1. user index page minor fix 
0. a office test server setting/deploying files 

==== start 2015-11-28 ====

## merged to master 2015-11-27

5. fix broken links on tag/hash-code
4. fix user tag list dup bug
3. fix user page follow/unfollow action bug 
2. event list page require js management 
1. event page require js management 
=== 2015 - 11 - 26 ======

1.修复django-sendcloud不能直接从setting读取配置的问题
2.补全丢失的settings信息
3.创建专题的时候隐藏top_tag，默认值为''
4.修改专题时隐藏top_tag
5.修改edm预览页面中静态图片地址

===== 2015 - 11 - 25 =======


2. event page add new recommendation section 
##Action remote/local db : need run sql  
        ALTER TABLE `core`.`core_show_editor_recommendation` 
        ADD COLUMN `section` VARCHAR(64) NOT NULL DEFAULT 'entity' AFTER `created_time`;

1. event page display update 

##Action local :merge master to dev -> launch pad functions 
##Action local :  ./manage.py syncdb --settings=......
   

=== 2015 11 24 ===

3. article_feed_read_counter deploy to 48 , cron tab 
2. fix API user like  500 error when user has no likes
1. entity detail page bug fix  , (a @property is lost when merge with judy's commit )

====== start 2015-11-23 ====

### merged to master  2015-11-23

1. 把用户页（喜爱，点评，文章，标签）加入requireJS
2. 搜索结果页加入requireJS

===== 2015 - 11 - 24 =======


3. m.guoku.com article page , wechat access , all link direct to http://www.guoku.com/download/
2. need deploy article_feed_counter_save.py to crontab
1. feed read count , need run sql  ,( already excuted on 10.0.2.90 core )

##ACTION : run sql , ( already run on 10.0.2.90   core )

ALTER TABLE `core`.`core_article` 
CHANGE COLUMN `read_count` `read_count` INT(10) UNSIGNED ZEROFILL NULL DEFAULT 0 ,
ADD COLUMN `feed_read_count` INT(10) UNSIGNED ZEROFILL NULL DEFAULT 0 AFTER `read_count`;


##ACTION : need run on production server FOR  sendCloud  : 

sudo pip install git+git://github.com/guoku/django-sendcloud@master

=== 2015 - 11 - 21 ====
1. 把记录搜索的方法record_search改成了用delay调用。


TODO : 现在移动端的标签还都是个人标签，是否需要改成全局标签

====  2015 - 11 -18 =====
2. new front-end for entity-detail page
1. add placeholder bug  quick fix for register page on IE8 

==== 2015 - 11  - 17  =====
0. 给module Search_History的record方法加了一点注释。
1. 把tag/articles下的页面加入RequireJS
2. 把category下的页面加入RequireJS，并作为滚动到页底自动加载
3. 在model research_history里的记录搜索函数，判断用户是否为游客的时候，换为一种更加安全的方式

1. 合并EDM到dev
2. 调整EDM内容样式
3. SD地址列表成员更新信息不能用update接口，需要先delete再add
4. EDM上线前需要先更新线上环境的django-sendcloud

************* start 2015-11-13 *************************

### merged to master 2015-11-12 

===== 2015 - 11 - 12 =======


2. remove 1111 gif on header 
1. article page dig
   
===== 2015 - 11 - 12 =======


	need run SQL  : 

	CREATE TABLE `core_search_history` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer,
    `key_words` varchar(255) NOT NULL,
    `search_time` datetime
	);
	ALTER TABLE `core_search_history` ADD CONSTRAINT 	`user_id_refs_id_371b5c0a` FOREIGN KEY (`user_id`) REFERENCES 	`core_gkuser` (`id`);

· 每次用户搜索的时候，都通过celery把搜索时间、关键字、用户记录下。

=== 2015-11-09 ================================


1. 修改了gruntfile.js，会自动把web/app下说有名称为*_app.js的文件build到web/jsbuild下，build后的名称为*_app_build.js；
2. 修复了message页，屏幕不断向下滚动时，会不断给页面增加空白块的bug；
3. 把discovery 页的js模块使用RequireJS加载。

=== 2015-11-6============================ 

3. article list page new front end 
2. add hidden img for app share , element id = 'share_img'
1. remove header render for article page 

关于客户端分享文章，图片问题

1. 客户端抓取页面（m.guoku.com/articles/id/）的第一张图片。
   现在第一张图片是双十一促销gif（in header）（新版 DEV 已经移除）

2. quick FIX 
   m.guoku.com 取消渲染 header 
   
3. more. 以后的 ios 版本可以用下面的方式拿到 图文 分享图片
   在图文详情页，有加入一个隐藏 div , ID="share_img"
   div 中有 img 元素作为文章分享图片。
   
   IOS NEED fix ：
4. 文章分享中 文章的地址， 应该是www.guoku.com的地址，而不是 m.guoku.com 的地址。
   
 

====== 2015 - 11 -5 ============


1. Event Top entity functions

    need run SQL  : 
    
    ALTER TABLE `core`.`core_event` 
    ADD COLUMN `toptag` VARCHAR(30) NOT NULL AFTER `created_datetime`;

=== 2015-11-4============================ 


1. event template adjust for 1111 event 

==== 2015-11-3 ===



给创建商品页添加了chosen插件。

### 2015-11-02 ===  merged to master =============================


6. IE8 compatible fix  -- done 
5. need fix scroll top header hidden bug  -- done 
4. top menu auto show/hide on scroll -- done
3. event page read red dot indicator -- done
2. sns bind page red dot indicator -- done
1. entity selection page autoload , paging --- done

note: the great performance leap(scroll frame rate) is to add backface-visibility: hidden; to fix elements.
==================== new frontend ==========
============= document in "前端JS开发" =======

5. 添加select插件chosen到后台的商品页。
    
4. dig functions for article (server side/Front End not implemented)

   *****  need syncdb *******, 
   new model :  Article_Dig

2. selection entity page js rebuild --- see ( new frontend )
1. to use assignment_tag on footer's friendly link
===== 2015 - 10 -22 == START =====

5. minor css adjusts

4. hide footer elements in xs screen

3. management selection articles list , add search 

2. entity detail page : add related article block

1. management entity management 
   a. add selection entity tab 
   b. add search for brand and entity title 
    
======== 2015 - 10 -18  start ===========

### 2015 - 10 -18 submmmit to master ========


1. 精选商品页中的待发布和已下架完全区分开；
2. 爬虫在爬到已下架的精选商品的时候，会把状态从商品更改为冻结。
 
=== 2015-10-15 ================================


6. add Event-related-article management 
   
   CREATE TABLE `core_event_related_articles` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `event_id` integer NOT NULL,
    `article_id` integer NOT NULL,
    UNIQUE (`event_id`, `article_id`)
    );
    ALTER TABLE `core_event_related_articles` ADD CONSTRAINT `article_id_refs_id_71111e46` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
    ALTER TABLE `core_event_related_articles` ADD CONSTRAINT `event_id_refs_id_9a1e89d0` FOREIGN KEY (`event_id`) REFERENCES `core_event` (`id`);

5. add article search , order by score 
4. change site.js , use /tag/name/  for tag entity page link
3. tag_entities_url url pattern capture change to (\w+) , to capture hash.
2. user index page - sidebar, user tag page , tag link updated to hash form. 
1. remove ga/ jiathis form article detail page, in m.guoku.com domains

=== 2015 - 10 - 12 === start =================


### 2015-10-12   MERGED TO  MASTER 
8. view optimize : use selected_related , prefetch_related to reduce sql hits.

7. block ISP ad injection

6. 更新 ariticle api , html_unescape article content , before sent to client 

5. 保存文章的时候提取相关商品列表保存

4. Article model 加入related_entities m2m 字段 (需要执行 SQL 语句)
   CREATE TABLE `core_article_related_entities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    UNIQUE (`article_id`, `entity_id`)
    );
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `entity_id_refs_id_8f4ed529` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `article_id_refs_id_c5544a89` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
    
    详情见 ： 日常开发文档／图文／文章 related entity.MD
    

3. 新增前台，标签 文章列表页
2. 文章列表页顶部加入置顶标签显示
1. 后台标签管理增加 置顶文章标签功能 
    
    (需要手动执行 SQL 语句)
    
    详情见 ： 日常开发文章／tag／实现 文章 tag 置顶 功能.MD

    ALTER TABLE `core`.`tag_tags` 
    ADD COLUMN `isTopArticleTag` TINYINT(1) NOT NULL DEFAULT 0 AFTER `image`;
   
    
=== 2015-10-10 =====  start ===========================