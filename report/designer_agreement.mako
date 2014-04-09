## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}

.list_main_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines,
.list_main_footers {
    padding: 0;
}
.list_main_footers {
    padding-top: 15px;
}
.list_main_lines td,
.list_main_footers td,
.list_main_footers th {
    border-style: none;
    text-align:left;
    font-size:12;
    padding:0;
}
.list_main_footers th {
    text-align:right;
}

td .total_empty_cell {
    width: 77%;
}
td .total_sum_cell {
    width: 13%;
}

.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}

.main_col1 {
    width: 40%;
}
td.main_col1 {
    text-align:left;
}
.main_col2,
.main_col3,
.main_col4,
.main_col6 {
    width: 10%;
}
.main_col5 {
    width: 7%;
}
td.main_col5 {
    text-align: center;
    font-style:italic;
    font-size: 10;
}
.main_col7 {
    width: 13%;
}

.right_table {
    right: 4cm;
    width:100%;
}

.std_text {
    font-size:12;
}

th.date {
    width: 90px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

.address .recipient .shipping .invoice {
    font-size: 12px;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        %if partner.parent_id:
            <tr><td class="name">${partner.parent_id.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for hetong in objects:
    <% setLang(hetong.partner_id.lang) %>

    <div class="hetong_right_no">
        <span>合同号: ${ hetong.name }</span>

    </div>
    <div class="hetong_header">
        <h1>委托设计合同</h1>

        <p>委托方：${ hetong.partner_id.name }（以下简称甲方）</p>
        <p>地  址：武汉市东湖开发区珞瑜路540号</p>
        <p>受托方：武汉德客天工品牌设计有限公司      （以下简称乙方）</p>
        <p>地  址：发展大道222号华南国际广场A座18楼 19~20号</p>


    </div>
    <div class="hetong_body">
        依据《中华人民共和国合同法》和有关法规的规定，在平等自愿的基础上，乙方接受甲方的委托，就甲方委托乙方进行《湖北宽善律师事务所》《武汉宽信股权投资基金管理有限公司》VI及画册设计、《武汉市合众创展科技小额贷款有限公司》VI设计事项，双方经协商一致，签订本合同，信守执行：
<h2>一、	VIS视觉识别系统及画册设计：</h2>

1） VIS视觉识别系统设计
<h3>1．	VI基础设计</h3>
1.1. 标准中英文字体<br/>
1.2.	标志标准色<br/>
1.3. 标志基本署式（全称）<br/>
1.4. 标志灰度应用规范<br/>
1.5. 标志明度应用规范<br/>
<h3>2．	VI应用设计</h3>
2.1. 名片<br/>
2.2.	纸杯<br/>
2.3. 信纸，备忘录<br/>
2.4. 胸牌<br/>
2.5. 信封、文件袋、手提袋<br/>
2.6. 合同规范式、邮件签名、PPT模板<br/>
2.7. 贺卡<br/>
2.8. 邀请函<br/>
<h3>3．VI手册三本</h3>
2） 画册设计
    预估每本24P，两本共计48P
<h2>二、委托设计费用及支付方式：</h2>
        <p>
1.  经双方协商，本合同总费用为：人民币伍万元整（￥ ${ hetong.contract_amount }元 ）.<br/>
2、在VI基础设计、VI应用设计全部制作完成，乙方将电子文档交甲方确认定稿后，甲乙双方签订合同，合同签订之日起三个工作日内甲方将前期设计费用人民币三万伍仟元整（￥35000元）通过现金、支票或银行转账方式支付到乙方公司账户。<br/>
3、在画册设计制作完成，乙方将电子文档交甲方确认定稿后三个工作日内，甲方将后期设计费用，即人民币壹万伍仟元整（￥15000.00元）支付到乙方公司账户。<br/>
        </p>
<h2>三、乙方设计作品的交付时间和方式。</h2>
        <p>
1、乙方应在本合同签订之日起三个工作日内将VI手册电子文档交付给甲方。<br/>
2、乙方交付的VI手册电子档经甲方确认无误后，乙方应及时制作样品，并将样品（三本VI手册）交付给乙方。<br/>
3、乙方应将画册电子档和画册样品交付给甲方，具体的交付时间由甲乙双方另行约定。<br/>
        </p>
<h2>四、甲方的权利和义务</h2>
        <p>


1．	甲方有权对乙方的设计提出建议和思路，以使乙方设计的作品更符合甲方企业文化内涵。<br/>
2． 有监督乙方工作过程和最终审核确定乙方工作质量的权利。在支付全部费后，享有乙方各项广告作品的最终所有权和使用权。<br/>
3．	有提供与创意设计有关的资料给乙方的义务。<br/>
4．	有按照双方约定的工作评价方法客观评价乙方工作的义务。<br/>
5．	有按合同规定时间付款的义务。<br/>
        </p>
<h2>五、乙方的权利和义务</h2>
        <p>
1.  不影响甲方利益的基础上，有权控制自己的工作程序和方式，并可要求甲方提供相应配合。<br/>
2． 有要求甲方不向第三方披露本合同各项费用等商业机密的权利。<br/>
3． 享有按合同规定时间获得报酬的权利。<br/>
4． 有按合同约定完成各项工作的义务。<br/>
5． 有为甲方保守商业秘密的义务。<br/>
6． 在甲方未支付工作费用前，乙方拥有广告作品的最终所有权和使用权。<br/>
7． 有权要求甲方提供相关资料和照片素材的权利。<br/>
        </p>
<h2>六、著作权</h2>
        <p>
甲方支付全部设计费后，享有乙方各项创作设计作品全部著作权。如：发表权、修改权、保护作品完整权、复制权、发行权、展览权、广播权、信息网络传播权及相关应由著作权人享有的其他权利。乙方享有其作品的署名权。
</p>
        <h2>七、其他约定事项</h2>
        <p>
1． 双方友好协议并达成共识可终止本合同。<br/>
2． 由于不可抗力因素（如政府干预、自然灾害等）导致合同无法执行，合同自然终止。<br/>
3.  因为非主观故意原因造成的进度延迟，由双方协商提出解决方案，如未对甲乙双方中的任何一方造成巨大经济、财产损失，本合同将不对任何一方进行处罚，并自动顺延其后的制作进度安排。<br/>
3.  本合同未尽事宜，双方可通过补充协议形式加以明确。补充协议与本合同享有同等法律效力。<br/>
        </p>
        <h2>八、合同纠纷解决方式</h2>
        <p>
            双方在本合同履行过程中发生争议，应协商解决，如协商无法解决，可向当地法院或经济仲裁机构申请仲裁。
        <p>
        <h2>九、	本合同一式贰份，甲乙双方各执壹份，具有同等法律效力（传真件、扫描件亦具有法律
效力）。
</h2>

    </div>
    <div class="hetong_footer">
        <div class="footer_line1">
    <p><span>甲方：武汉市合众创展科技小额贷款有限公司</span> <span>  乙方： 武汉德客天工品牌设计有限公司</span></p>

        </div>
        <div class="footer_line2">

代表人签章：                               代表人签章：
        </div>
        <div class="footer_line3">

联系电话：                                 联系电话：


        </div>
        <div class="footer_line4">
二〇一三年   月    日                      二〇一三年     月    日

        </div>
        <div class="footer_end"></div>

    </div>
    <p style="page-break-after:always"/>
    %endfor
</body>
</html>
