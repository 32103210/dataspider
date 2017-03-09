from bs4 import BeautifulSoup

import pandas as pd


def TableDataProcess(text, name):
    # 定义了一个100*100的二维数组
    rows = 100
    cols = 100
    matrix = [[None] * cols for i in range(rows)]
    title = text.select('#bttab  > tr')
    tab_tr = text.select('#maintab > tr')
    num = len(tab_tr)
    col = 0  # 列数
    for i in range(num + 3):
        if i == 0:
            matrix[i][0] = name
            continue
        if len(title) == 3 and i == 1:
            unit = BeautifulSoup(str(title[2]), 'lxml')
            unit_text = unit.select('td')[0]
            matrix[i][0] = unit_text.get_text()
            continue
        # 将表头的出来和表主体的处理合在一起了
        else:
            if i >= len(tab_tr)+2:
                break
            tr_soup = BeautifulSoup(str(tab_tr[i - 2]), 'lxml')
            tdList = tr_soup.select('td')
            # print(tdList)
            for k, j in enumerate(tdList):
                if matrix[i][k] != None:
                    continue
                if k ==4:
                    col = len(tdList)
                rowspan = 0
                colspan = 0
                # print(j.get('rowspan'))
                if j.get('rowspan') != None:
                    rowspan = int(j.get('rowspan'))
                    # print(rowspan)
                if j.get('colspan') != None:
                    colspan = int(j.get('colspan'))
                # print(j.get_text())
                for index in range(rowspan+1):
                    matrix[i + index][k] = j.get_text()
                for index in range(colspan+1):
                    matrix[i][k + index] = j.get_text()
    result = pd.DataFrame(matrix)
    return result

html = """""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <base href="http://data.gzstats.gov.cn:80/gzStat1/">
    <title>查看报表</title>
    <meta http-equiv="pragma" content="no-cache">
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="expires" content="0">
    <meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
    <meta http-equiv="description" content="This is my page">

<LINK href="/gzStat1/css/default.css" type="text/css" rel="stylesheet">
<LINK href="/gzStat1/css/tj.css" type="text/css" rel="stylesheet">
<script src="/gzStat1/chaxun/js/iframeauto.js" ></script>
<script src="/gzStat1/js/check.js"></script>
<script language="JavaScript" type="">
<!--
var openwin;
var Intval;
var isclicked=false;
var errid;
var errmsg;
errid=0;
errmsg="";
var btRlist=new Array();
var hzflist=new Array();



function tabstyle(align,bgColor,borderColor,border,borderLeft,borderRight,borderTop,borderBottom,cellspacing,cellpadding,width)
{
    this.align=align;//左右对齐方式
	this.bgColor=bgColor;//单元格背景色
	this.borderColor=borderColor;
	this.border=border;
	this.borderLeft=borderLeft;//左边框
	this.borderRight=borderRight;//右边框
	this.borderTop=borderTop;//上边框
	this.borderBottom=borderBottom;//下边框
	this.cellspacing=cellspacing;
	this.cellpadding=cellpadding;
	this.width=width;//单元格宽度
    return this;
}

function mainRow(mbid,flag,no,rowsx,fzm)
{
   this.mbid=mbid;
   this.flag=flag;
   this.no=no;
   this.rowsx=rowsx;
   this.fzm=fzm;
   this.celllist=new Array();
   this.condilist=new Array();
   return this;
}

function mainCol(width)
{
   this.width=width;
   this.sxlist=new Array();//维度属性(设置在单元格中的)
   this.condilist=new Array();
   return this;
}
function mainCell(mbstr,flag,align,valign,bgColor,color,borderLeft,borderRight,borderTop,borderBottom,fontSize,fontFamily,fontWeight,gs,value,oldvalue,isdata,rowspan,colspan,kj)
{
   this.mbstr=mbstr;//模板字符串
   this.flag=flag;//标记单元格是合并单元格"B"还是普通单元格"A"
   this.align=align;//左右对齐方式
   this.valign=valign;//上下对齐方式
   this.bgColor=bgColor;//单元格背景色
   this.color=color;//单元格前景颜色
   this.borderLeft=borderLeft;//左边框
   this.borderRight=borderRight;//右边框
   this.borderTop=borderTop;//上边框
   this.borderBottom=borderBottom;//下边框
   this.fontSize=fontSize; //字体大小
   this.fontFamily=fontFamily;//字体
   this.fontWeight=fontWeight;//字体宽度
   this.gs=gs;//公式代号
   this.value=value;//计算结果
   this.oldvalue=oldvalue;//原值
   this.isdata=isdata;//是否为数据格
   this.rowspan=rowspan;//行合并行数
   this.colspan=colspan;//列合并列数
   this.kj=kj;//是否插入在模板中插入一文本框,主要用于报表脚.
   this.sxlist=new Array();//维度属性(设置在单元格中的)
   this.condilist=new Array();
   return this;
}
function SQLObj(id,code,name,sqltype,info,conditionnum,valfield,groupby)
{
   this.id=id;
   this.code=code;//变量编号
   this.name=name;//变量名称
   this.sqltype=sqltype;//变量类别:"0"基础数据取数变量;"1"综合数据取数变量;"2"名称库取数变量(即从TJ_101表取数)
   this.info=info;//说明
   this.conditionnum=conditionnum;//条件字段个数
   this.valfield=valfield;//要查询的列名
   this.groupby=groupby;//聚合类型:count求记录个数,sum求和,avg求平均,"":不聚合
   this.conditionList=new Array();
   return this;
}
function condition(field,fieldname,fieldtype,conditiontype)
{
   this.field=field;//字段名
   this.fieldname=fieldname;
   this.fieldtype=fieldtype;//"T"为字符型;"N"为数字型
   this.conditiontype=conditiontype;//条件类别:0为具体设置;1为模板设置时设置条件;2为计算某期报表时动态对接表头属性条件
   this.condilist=new Array();
   return this;
}
function condi(and_or,lkh,czf,vals,valchns,rkh)
{
   this.and_or=and_or;
   this.lkh=lkh;
   this.czf=czf;
   this.vals=vals;
   this.valchns=valchns;
   this.rkh=rkh;
   return this;
}
function gsObj(code,name,gs,info,point,jldw)
{
   this.code=code;
   this.name=name;
   this.gs=gs;
   this.info=info;
   this.point=point;
   this.jldw=jldw;
   return this;
}

//字段元数据对象
function hz_data_metafield(field,type,name,wdk)
{
   this.field=field;
   this.type=type;
   this.name=name;
   this.wdk=wdk;
   this.sourseflag=0;
   return this;
}

//设置在模板中的字段属性对象
function fieldsx(fieldid,fieldname,val,code,valchn,flag)
{
   this.fieldid=fieldid;
   this.fieldname=fieldname;
   this.val=val;
   this.code=code;
   this.valchn=valchn;
   this.flag=flag;
   this.condifs=new Array();
   this.condiczfs=new Array();
   this.sourseflags=new Array();
   return this;
}

function key()
{
  return false;
}
function key_()
{
}



      btRlist[0]=new mainRow('33283','A',1,'','');

          btRlist[0].celllist[0]=new mainCell('1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)','A','center','middle','#FFFFFF','#000000',1,1,1,1,16,'宋体','bold','','','','1',1,6,'');

             btRlist[0].celllist[0].sxlist[0]=new fieldsx('YEAR','年份','','','2016','');

                     btRlist[0].celllist[0].sxlist[0].condifs[0]="YEAR";
                     btRlist[0].celllist[0].sxlist[0].condiczfs[0]="=";
                     btRlist[0].celllist[0].sxlist[0].sourseflags[0]="-1";

          btRlist[0].celllist[1]=new mainCell('','B','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[0].celllist[2]=new mainCell('','B','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[0].celllist[3]=new mainCell('','B','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[0].celllist[4]=new mainCell('','B','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[0].celllist[5]=new mainCell('','B','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

      btRlist[1]=new mainRow('33283','A',2,'','');

          btRlist[1].celllist[0]=new mainCell('Administrative&nbsp;Divisions&nbsp;(Year-end&nbsp;of&nbsp;2015)','A','center','middle','#FFFFFF','#000000',0,0,0,0,15,'宋体','bold','','','','1',1,6,'');

          btRlist[1].celllist[1]=new mainCell('','B','left','middle','#ffffff','#000000',1,1,1,1,12,'宋体','normal','','','','0',1,1,'');

          btRlist[1].celllist[2]=new mainCell('','B','left','middle','#ffffff','#000000',1,1,1,1,12,'宋体','normal','','','','0',1,1,'');

          btRlist[1].celllist[3]=new mainCell('','B','left','middle','#ffffff','#000000',1,1,1,1,12,'宋体','normal','','','','0',1,1,'');

          btRlist[1].celllist[4]=new mainCell('','B','left','middle','#ffffff','#000000',1,1,1,1,12,'宋体','normal','','','','0',1,1,'');

          btRlist[1].celllist[5]=new mainCell('','B','left','middle','#ffffff','#000000',1,1,1,1,12,'宋体','normal','','','','0',1,1,'');

      btRlist[2]=new mainRow('33283','A',3,'','');

          btRlist[2].celllist[0]=new mainCell('单位:个','A','left','middle','#FFFFFF','#000000',0,0,0,0,12,'宋体','normal','','','','1',1,1,'');

          btRlist[2].celllist[1]=new mainCell('','A','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[2].celllist[2]=new mainCell('','A','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[2].celllist[3]=new mainCell('','A','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[2].celllist[4]=new mainCell('','A','left','middle','#FFFFFF','#000000',1,1,1,1,12,'宋体','normal','','','','1',1,1,'');

          btRlist[2].celllist[5]=new mainCell('(unit)','A','left','middle','#FFFFFF','#000000',0,0,0,0,12,'宋体','normal','','','','1',1,1,'');

        hzflist[0]=new hz_data_metafield('ZBID','T','指标ID','RPT_INDICATION');

        hzflist[1]=new hz_data_metafield('YEAR','T','年份','');

        hzflist[2]=new hz_data_metafield('MONTH','T','月/季/半年度','');

        hzflist[3]=new hz_data_metafield('VALUE','N',' 指标值','');

        hzflist[4]=new hz_data_metafield('JLDW','T','计量单位','');

        hzflist[5]=new hz_data_metafield('WD_DZM','T','行政区划','TJ_WDK_DZM');

        hzflist[6]=new hz_data_metafield('WD_INDUSTRY','T','国民经济行业类别','TJ_WDK_INDUSTRY');

        hzflist[7]=new hz_data_metafield('SYQGDFL','T','输油气管道分类','TJ_WDK_SYGDFL');

        hzflist[8]=new hz_data_metafield('YSFL','T','运输分类','TJ_WDK_YSFL');

        hzflist[9]=new hz_data_metafield('NYFL','T','能源分类','TJ_WDK_NYFL');

        hzflist[10]=new hz_data_metafield('SPFL','T','商品分类','TJ_WDK_SPFL');

        hzflist[11]=new hz_data_metafield('HWFL','T','货物分类','TJ_WDK_HWFL');

        hzflist[12]=new hz_data_metafield('QZGYFL','T','轻重工业分类','TJ_WDK_QZGYFL');

        hzflist[13]=new hz_data_metafield('LYXL','T','旅游线路','TJ_WDK_LYXL');

        hzflist[14]=new hz_data_metafield('ZSJSES','T','珠三角十二市(区)','TJ_WDK_ZSJSES');

        hzflist[15]=new hz_data_metafield('JMJTFL','T','居民家庭分类','TJ_WDK_JMJTSRFL');

        hzflist[16]=new hz_data_metafield('XXFL','T','学校分类','TJ_WDK_XXFL');

        hzflist[17]=new hz_data_metafield('LYY','T','零售业','TJ_WDK_LYY');

        hzflist[18]=new hz_data_metafield('PFY','T','批发业','TJ_WDK_PFY');

        hzflist[19]=new hz_data_metafield('GMYSGYQY','T','规模以上工业企业','TJ_WDK_GMYSGYQY');

        hzflist[20]=new hz_data_metafield('HYLB','T','行业类别','TJ_WDK_INDUSTRY');

        hzflist[21]=new hz_data_metafield('ZYGYCP','T','主要工业产品','TJ_WDK_ZYGYCP');

        hzflist[22]=new hz_data_metafield('ZCZFZ','T','总产值分组','TJ_WDK_ZCZFZ');

        hzflist[23]=new hz_data_metafield('GDZCYJFZ','T','固定资产原价分组','TJ_WDK_GDZCYJFZ');

        hzflist[24]=new hz_data_metafield('LSZEFZ','T','利税总额分组','TJ_WDK_LSZEFZ');

        hzflist[25]=new hz_data_metafield('ZGRSFZ','T','职工人数分组','TJ_WDK_ZGRSFZ');

        hzflist[26]=new hz_data_metafield('LKFL','T','旅客分类','TJ_WDK_LKFL');

        hzflist[27]=new hz_data_metafield('RJCKYJSJKQK','T','软件出口与技术进口情况','TJ_WDK_RJCKYJSJKQK');

        hzflist[28]=new hz_data_metafield('DWJJHZYWQK','T','对外经济合作业务情况','TJ_WDK_DWJJHZYWQK');

        hzflist[29]=new hz_data_metafield('AMYXFMYXFL','T','按贸易性非贸易性分类','TJ_WDK_AMYXFMYXFL');

        hzflist[30]=new hz_data_metafield('TJZS','T','统计指数','TJ_WDK_TJZS');

        hzflist[31]=new hz_data_metafield('WD_CITY','T','城市','TJ_WDK_540367737339459852');

        hzflist[32]=new hz_data_metafield('NYJGZHFL','T','能源加工转换分类','TJ_WDK_NYJGZHFL');

        hzflist[33]=new hz_data_metafield('KJ','T','口径','TJ_WDK_KJ');

        hzflist[34]=new hz_data_metafield('JCKFL','T','进出口分类','TJ_WDK_JCKFL');

        hzflist[35]=new hz_data_metafield('GMJJLX','T','国民经济类型','TJ_WDK_GMJJLX');

        hzflist[36]=new hz_data_metafield('FDCKF','T','房地产开发类型','TJ_WDK_FDC');

        hzflist[37]=new hz_data_metafield('GXZYFL','T','高校专业分类','TJ_WDK_GXZYFL');

        hzflist[38]=new hz_data_metafield('XLQK','T','学历情况','TJ_WDK_XLQK');

        hzflist[39]=new hz_data_metafield('ZLFL','T','专利分类','TJ_WDK_ZLFL');

        hzflist[40]=new hz_data_metafield('ZYJSRYFL','T','专业技术人员分类','TJ_WDK_ZYJSRYFL');

        hzflist[41]=new hz_data_metafield('SSKXFL','T','市属科协分类','TJ_WDK_SSKXFL');

        hzflist[42]=new hz_data_metafield('JSLYFL','T','技术领域分类','TJ_WDK_JSLYFL');

        hzflist[43]=new hz_data_metafield('BXXM','T','保险项目','TJ_WDK_BXXM');

        hzflist[44]=new hz_data_metafield('GMJJHYFZ','T','国民经济行业分组','TJ_WDK_GMJJHYFZ');

        hzflist[45]=new hz_data_metafield('NCPFL','T','农产品分类','TJ_WDK_NCPFL');

        hzflist[46]=new hz_data_metafield('SPJYSCMC','T','商品交易市场名称','TJ_WDK_SPJYSCMC');

        hzflist[47]=new hz_data_metafield('SCLX','T','市场类型','TJ_WDK_SCLX');

        hzflist[48]=new hz_data_metafield('SQ','T','时期','TJ_WDK_SQ');

        hzflist[49]=new hz_data_metafield('JCKSPFL','T','进出口商品','TJ_WDK_JCKSPFL');

        hzflist[50]=new hz_data_metafield('WZMC','T','物资名称','TJ_WDK_WZMC');

        hzflist[51]=new hz_data_metafield('AJJLXF','T','按经济类型分','TJ_WDK_AJJLXF');

        hzflist[52]=new hz_data_metafield('BGJB','T','宾馆级别','TJ_WDK_BGJB');

        hzflist[53]=new hz_data_metafield('QGZYCS','T','全国主要城市','TJ_WDK_QGZYCS');

        hzflist[54]=new hz_data_metafield('GDZCTZLB','T','固定资产投资类别','TJ_WDK_GDZCTZFL');

        hzflist[55]=new hz_data_metafield('DJZCQYLX','T','登记注册企业类型','TJ_WDK_DJZCQYLX');

        hzflist[56]=new hz_data_metafield('CSGGJTLX','T','城市(市区)公共交通类型','TJ_WDK_CSGGJTLX');

        hzflist[57]=new hz_data_metafield('CZDWFL','T','城镇单位分类','TJ_WDK_CZDWFL');

        hzflist[58]=new hz_data_metafield('JMXFXSPFL','T','居民消费性商品分类','TJ_WDK_JMXFXSPFL');

        hzflist[59]=new hz_data_metafield('YXMC','T','院校名称','TJ_WDK_YXMC');

        hzflist[60]=new hz_data_metafield('QYGMFL','T','企业规模分类','TJ_WDK_QYGMFL');

        hzflist[61]=new hz_data_metafield('YLJG','T','卫生机构','TJ_WDK_YLJG');

        hzflist[62]=new hz_data_metafield('ZFJG','T','政府机构','TJ_WDK_ZFJG');

        hzflist[63]=new hz_data_metafield('SHSPGMLLYYFP','T','社会商品购买力来源与分配','TJ_WDK_SHSPGMLLYYFP');

        hzflist[64]=new hz_data_metafield('ZYNYHY','T','主要农业行业','TJ_WDK_ZYNYHY');

        hzflist[65]=new hz_data_metafield('NF','T','年份','TJ_WDK_NF');

        hzflist[66]=new hz_data_metafield('CPXSLX','T','产品销售流向','TJ_WDK_CPXSLX');

        hzflist[67]=new hz_data_metafield('SPSCDQFL','T','商品市场地区分类','TJ_WDK_SPSCDQFL');

        hzflist[68]=new hz_data_metafield('MYQY','T','贸易企业','TJ_WDK_MYQY');

        hzflist[69]=new hz_data_metafield('NCJJJYFS','T','农村经济经营方式','TJ_WDK_NCJJJYFS');

        hzflist[70]=new hz_data_metafield('JCKSPFLJE','T','进出口商品分类','TJ_WDK_JCKSPFLJE');

        hzflist[71]=new hz_data_metafield('HWDFL','T','货物到发量','TJ_WDK_HWDFL');

        hzflist[72]=new hz_data_metafield('GBDQ','T','国别与地区','TJ_WDK_GBDQ');

        hzflist[73]=new hz_data_metafield('JMZFFL','T','居民住房分类','TJ_WDK_JMZFFL');

        hzflist[74]=new hz_data_metafield('WD_DJZCLX','T','登记注册类型','TJ_WDK_DJZCLX');

        hzflist[75]=new hz_data_metafield('XEYSLSD','T','限额以上连锁店(公司)','TJ_WDK_XEYSLSD');

        hzflist[76]=new hz_data_metafield('SPJYSCCJQK','T','商品交易市场成交情况','TJ_WDK_SPJYSCCJQK');

        hzflist[77]=new hz_data_metafield('GMJJLB2','T','国民经济类别2','TJ_WDK_GMJJLB2');

        hzflist[78]=new hz_data_metafield('ZDJSXMFL','T','重点建设项目分类','TJ_WDK_ZDJSXMFL');

        hzflist[79]=new hz_data_metafield('GCYT','T','按工程用途分','TJ_WDK_GCYT');

        hzflist[80]=new hz_data_metafield('ZGXT','T','主管系统分类','TJ_WDK_ZGXT');

        hzflist[81]=new hz_data_metafield('SPMYFL','T','商品贸易类型','TJ_WDK_SPMYLX');

        hzflist[82]=new hz_data_metafield('LYYSRQKFL','T','旅游业收入情况分类','TJ_WDK_LYYSRQKFL');

        hzflist[83]=new hz_data_metafield('JSSCJY','T','技术市场交易','TJ_WDK_JSSCJY');

        hzflist[84]=new hz_data_metafield('NCPCL','T','农产品产量','TJ_WDK_NCPCL');

        hzflist[85]=new hz_data_metafield('WD_KGQK','T','企业控股情况','TJ_WDK_KGQK');

        hzflist[86]=new hz_data_metafield('WD_LSGX','T','隶属关系','TJ_WDK_LSGX');

        hzflist[87]=new hz_data_metafield('WD_ZZJGLX','T','机构类型','TJ_WDK_ZZJGLX');

        hzflist[88]=new hz_data_metafield('WD_AREA','T','国别(地区)','TJ_WDK_AREA');

        hzflist[89]=new hz_data_metafield('WD_YDK','T','月度库维度','TJ_WDK_327329012327329012');

        hzflist[90]=new hz_data_metafield('WD_SQ','T','时期','TJ_WDK_612180385612180385');

        hzflist[91]=new hz_data_metafield('WD_GXLLD','T','贡献率和拉动','TJ_WDK_GXLLD');

        hzflist[92]=new hz_data_metafield('WD_NYXFFL','T','能源消费分类','TJ_WDK_NYXFFL');

        hzflist[93]=new hz_data_metafield('RATETIME','T','人民币存贷款利率调整时间','TJ_WDK_RATETIME');

        hzflist[94]=new hz_data_metafield('DEPOTYPE','T','人民币存款类型(包括期限)','TJ_WDK_DEPOTYPE');

        hzflist[95]=new hz_data_metafield('LOANSTIME','T','人民币贷款期限','TJ_WDK_LOANSTIME');

        hzflist[96]=new hz_data_metafield('WBLX','T','外币类型','TJ_WDK_WBLX');

        hzflist[97]=new hz_data_metafield('XWQK','T','学位情况','TJ_WDK_XWQK');

        hzflist[98]=new hz_data_metafield('NCC','T','按城乡分','TJ_WDK_CX');

        hzflist[99]=new hz_data_metafield('FDCFWYT','T','房地产房屋用途','TJ_WDK_080X203');

        hzflist[100]=new hz_data_metafield('JSXZ','T','按建设性质分','TJ_WDK_AJSXZF');

        hzflist[101]=new hz_data_metafield('GC','T','按构成分','TJ_WDK_AGCF');

        hzflist[102]=new hz_data_metafield('CYHDDW','T','产业活动单位分类','TJ_WDK_CYHDDW');



function showMb()
{
    var f=document.forms[0];
    var linkstr="/gzStat1/tj_rpt_mb_metatabAction.do?method=showMb&ID=33283&RPTID=TJ_RPT_400165139747601058&PRINTCONF=TRUE";
    window.open(linkstr,"_blank");
}


function displayRpt()
{
   if(isclicked)return;
    var f=document.forms[0];
    isclicked=true;
    document.body.style.cursor = 'wait';
    dispinfo_("查询报表,请稍等...");
    f.action="/gzStat1/yearqueryAction.do?method=displayRpt";
    f.target="_self";
    f.submit();
}

function InitAjax(){
var ajax=false; 　
try { 　　
  ajax = new ActiveXObject("Msxml2.XMLHTTP"); 　
} catch (e) { 　　
	try { 　　　
	  ajax = new ActiveXObject("Microsoft.XMLHTTP"); 　　
	} catch (E) { 　　　
	  ajax = false; 　　
	} 　
}　
if (!ajax && typeof XMLHttpRequest!='undefined') { 　　
  ajax = new XMLHttpRequest(); 　
} 　
return ajax;
}



function dispRpt()
{
    displayRpt();
}


var year=2017;
var datatype=4;
var month=0;
var maxmonth=0;


function changeYear(obj)
{
   if(datatype!=4)
   {
     var thyear=parseInt(obj.options[obj.selectedIndex].value);
     var mobj=document.forms[0].MONTH;
     var smindex=mobj.selectedIndex;
     if(thyear<year)
     {
        mobj.options.length=maxmonth;
        for(var m=1;m<=maxmonth;m++)
        {
          mobj.options[m-1].value=m<10?"0"+m:""+m;
          if(datatype==1)
             mobj.options[m-1].text=(m<10?"0"+m:""+m)+"月";
          else if(datatype==2)
             mobj.options[m-1].text="第"+m+"季度";
          else
             mobj.options[m-1].text=(m==1?"上":"下")+"半年";
        }
        mobj.options[smindex].selected=true;
     }else
     {
         mobj.options.length=month;
        for(var m=1;m<=month;m++)
        {
          mobj.options[m-1].value=m<10?"0"+m:""+m;
          if(datatype==1)
             mobj.options[m-1].text=(m<10?"0"+m:""+m)+"月";
          else if(datatype==2)
             mobj.options[m-1].text="第"+m+"季度";
          else
             mobj.options[m-1].text=(m==1?"上":"下")+"半年";
        }
        if(smindex<month)
        {
          mobj.options[smindex].selected=true;
        }else
        {
          mobj.options[month-1].selected=true;
        }
     }
   }
   dispRpt();
}


function toback()
{
  var Path;
  Path="/gzStat1/yearqueryAction.do?method=det_Title";
  document.forms[0].action=Path;
  document.forms[0].target="_self";
  document.forms[0].submit();
}

function dispinfo(info)
{
  if(info!="")
  {
     var html="<table border=\"2\" onmouseout=\"hidinfoDiv();\" width=\"250px\" cellpadding=\"2\" bordercolor=\"#FBFB8C\" style=\"border-collapse: collapse;table-layout:fixed;word-break:break-all; word-wrap: break-word\"><tr><td><b><font color='red'>出错信息：</font></b>"+info+"</td></tr></table>";
     infoDiv.innerHTML=html;
     showinfoDiv();
  }
}

function dispinfo_(info)
{
  if(info!="")
  {
     var html="<table border=\"2\" width=\"250px\" cellpadding=\"2\" bordercolor=\"#FBFB8C\" style=\"border-collapse: collapse;table-layout:fixed;word-break:break-all; word-wrap: break-word\"><tr><td><b><font color='red' style=\"font-size:14px\">"+info+"</font></b></td></tr></table>";
     infoDiv.innerHTML=html;
     showinfoDiv_();
  }
}
function showinfoDiv()
{
   var theRealTop=parseInt(document.body.scrollTop);
   var theRealLeft=parseInt(document.body.scrollLeft);
   infoDiv.style.display="block";
   var calEx=event.x;
   var calEy=event.y;
   var cx=document.body.clientWidth-infoDiv.clientWidth-5;
   var cy=document.body.clientHeight-infoDiv.clientHeight-5;
   infoDiv.style.posLeft=((calEx<cx)?calEx:cx)+theRealLeft+10;
   infoDiv.style.posTop=((calEy<cy)?calEy:cy)+theRealTop-30;

}

function showinfoDiv_()
{
   infoDiv.style.display="block";
   infoDiv.style.posLeft=200;
   infoDiv.style.posTop=150;

}
function hidinfoDiv()
{
  infoDiv.style.display="none";
}

function download(fn,path,fnchn,rptname)
{	var f=document.forms[0];
   f.action="/gzStat1/download?filename="+fn+"&filepath="+path+"&filenamechn="+fnchn+"&RPTNAME="+rptname;
   f.target="_blank";
   f.submit();
}


//保持搜索框在相对位置
function keep(theWantTop,theWantLeft)
{
  theRealTop=parseInt(document.body.scrollTop);
  theTrueTop=theWantTop+theRealTop;
  SearchBar.style.top=theTrueTop;
  theRealLeft=parseInt(document.body.scrollLeft);
  theTrueLeft=theWantLeft+theRealLeft;
  SearchBar.style.Left=theTrueLeft;
}
//层显示和隐藏
function Show(divid) {
	divid.filters.revealTrans.apply();
	divid.style.visibility = "visible";
    SearchBar.style.posLeft=200;
    SearchBar.style.posTop=150;
    divid.filters.revealTrans.play();
}

function Hide(divid) {
	divid.filters.revealTrans.apply();
	divid.style.visibility = "hidden";
	divid.filters.revealTrans.play();
}
</script>
</head>
<body bgcolor="#ffffff">

<form name="yearqueryForm" method="POST" action="/gzStat1/yearqueryAction.do?method=displayRpt">
        <input type="hidden" name="ACTFLAG" value="3"/>
        <input type="hidden" name="RPTID" value="TJ_RPT_400165139747601058"/>
        <input type="hidden" name="RPTNAME" value="1-1 琛???垮?哄??"/>
        <input type="hidden" name="FLTITLE" value="2016-12-06/绗?涓?绡????缁煎??"/>

		<input type="hidden" name="flId" value=""/>
 		<input type="hidden" name="flname" value=""/>
 		<input type="hidden" name="title" value=""/>
 		<input type="hidden" name="fbDate" value=""/>
 		<input type="hidden" name="falg" value=""/>
 		<input type="hidden" name="year" value=""/>
 		<input type="hidden" name="lmId" value=""/>
	 <table width="100%" height=20 align="center" cellpadding="0" cellspacing="0">
        <tr>
          <td width="1%">&nbsp;</td>
          <td width="98%"  valign="bottom" colspan="3" class="date" height="20">
           <img src="/gzStat1/system/images/bullet_main_02.gif">&nbsp;1-1 琛???垮?哄??<img src="/gzStat1/system/images/bullet_main_02.gif">&nbsp;查看报表
          <td width="1%"></td>
        </tr>
  </table>
  <table width="100%" id=printtab align="center" cellpadding="0" cellspacing="0">

        <tr>
          <td width="3%">&nbsp;</td>
          <td width="95%" align='left'  valign="bottom"  class="date" height="20">

              &nbsp;<input type="button" value="导出" onclick="download('64864.htm','rptfile','1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)_2016年.xls','1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)');" class="btnview" onmouseover="this.className='btnn';this.style.cursor = 'hand';" onmouseout="this.className='btnview';"/>
              &nbsp;<input type="button" value="打印" onclick="preview();" class="btnview" onmouseover="this.className='btnn';this.style.cursor = 'hand';" onmouseout="this.className='btnview';"/>
              &nbsp;<input type="button" value="返回" onclick="toback();" class="btnview" onmouseover="this.className='btnn';this.style.cursor = 'hand';" onmouseout="this.className='btnview';"/>

            <br>
           <hr size=1 style='width:100%;' color='#000000'>
          </td>
          <td width="2%"></td>
        </tr>

        <tr>
<td colspan='3'>
<table id=bttab  width='650' cellspacing="1" cellpadding="1" align="center" border="0px" bordercolor="#0079BB" bgColor="#FFFFFF" style="border-collapse: collapse;">

     <tr style="height:22">

             <td width='96%' colspan='6' align='center' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:16; font-weight:bold;'>
             1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)
             <br>
              <select name='YEAR'  onchange='changeYear(this);'>
<option value='2017'>统计年鉴2017</option>
<option value='2016' selected='selected'>统计年鉴2016</option>
<option value='2015'>统计年鉴2015</option>
<option value='2014'>统计年鉴2014</option>
<option value='2013'>统计年鉴2013</option>
<option value='2012'>统计年鉴2012</option>
<option value='2011'>统计年鉴2011</option>
<option value='2010'>统计年鉴2010</option>
<option value='2009'>统计年鉴2009</option>
<option value='2008'>统计年鉴2008</option>
<option value='2007'>统计年鉴2007</option>
<option value='2006'>统计年鉴2006</option>
<option value='2005'>统计年鉴2005</option>
<option value='2004'>统计年鉴2004</option>
<option value='2003'>统计年鉴2003</option>
<option value='2002'>统计年鉴2002</option>
<option value='2001'>统计年鉴2001</option>
<option value='2000'>统计年鉴2000</option>
</select>

              </td>

          </tr>

     <tr style="height:22">

                <td width='96%' colspan='6' align='center' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:15; font-weight:bold;'>
                 Administrative&nbsp;Divisions&nbsp;(Year-end&nbsp;of&nbsp;2015)

                </td>

          </tr>

     <tr style="height:22">

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>
                 单位:个

                </td>

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>


                </td>

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>


                </td>

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>


                </td>

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>


                </td>

                <td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>
                 (unit)

                </td>

          </tr>

 </table>
</td>
</tr>
<tr>
<td colspan='3'>
<input type='hidden' name='RPTFID' value='64864'>

   <table id='ttab' align="center" style="border:0px;width:650"><tr><td width='96%' colspan='6' align='center' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:16; font-weight:bold;'>1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)<br><font style='font-size:12px'>2016年</font></td></tr><tr><td width='96%' colspan='6' align='center' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:15; font-weight:bold;'>Administrative&nbsp;Divisions&nbsp;(Year-end&nbsp;of&nbsp;2015)</td></tr><tr><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>单位:个</td><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'></td><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'></td><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'></td><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'></td><td width='16%' align='left' valign='middle' bgColor='#FFFFFF' style='color:#000000;font-family:宋体;font-size:12; font-weight:normal;'>(unit)</td></tr></table><table id=maintab  cellspacing="1" cellpadding="1" align="center" border="1px" bordercolor="#0079BB" bgColor="#FFFFFF" style="border-collapse: collapse;border-left:0px solid #0079BB;border-right:0px solid #0079BB;border-top:1px solid #0079BB;border-bottom:1 px solid #0079BB"><tr style='height:20'><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:0px solid #0079BB; border-right:1px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>地区</td><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:1px solid #0079BB; border-right:1px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>Districts</td><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:1px solid #0079BB; border-right:1px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>街道办事处StreetCommunities</td><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:1px solid #0079BB; border-right:1px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>镇Towns</td><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:1px solid #0079BB; border-right:1px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>社区居委会CommunityCommittees</td><td width='100px' align='center' valign='middle' style='color:#000000; border-bottom:1px solid #0079BB; border-left:1px solid #0079BB; border-right:0px solid #0079BB; border-top:1px solid #0079BB;font-family:宋体;font-size:12; font-weight:bold;' bgColor='#D5D5D5'>村民委员会Villagers’Committees</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#F5F5F5'>合&nbsp;&nbsp;&nbsp;计</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#F5F5F5'>Total</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>136</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>34</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>1494</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>1144</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#F5F5F5'>　荔湾区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#F5F5F5'>　Liwan</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>22</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'></td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'>186</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' bgColor='#FFFFFF'></td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　越秀区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Yuexiu</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>18</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>222</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　海珠区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Haizhu</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>18</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>257</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　天河区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Tianhe</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>21</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>208</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'></td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　白云区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Baiyun</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>18</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>4</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>250</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>118</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　黄埔区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Huangpu</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>14</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>1</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>96</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>28</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　番禺区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Panyu</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>11</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>5</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>90</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>177</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　花都区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Huadu</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>4</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>6</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>54</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>188</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　南沙区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Nansha</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>3</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>6</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>28</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>128</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>&nbsp;&nbsp;从化区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Conghua</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>3</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>5</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>46</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>221</td></tr><tr style='height:20'><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>&nbsp;&nbsp;增城区</td><td width='100px' align='left' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#F5F5F5'>　Zengcheng</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>4</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>7</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>57</td><td width='100px' align='right' valign='middle' style='color:#000000; border-bottom:0px solid #0079BB; border-left:0px solid #0079BB; border-right:0px solid #0079BB; border-top:0px solid #0079BB;font-family:宋体;font-size:12; font-weight:normal;' nowrap='nowrap' bgColor='#FFFFFF'>284</td></tr></table><br/><br/>

</td></tr>
 </table>
 <textarea name="printtxt" style="display:none"></textarea>
</form>
<div id='infoDiv'  onmousemove="this.style.display='';"  style='z-index:auto;border: 1px outset #ffffff;position: absolute;display: none;background-color:#FBFB8C;width:250px'></div>
<div id="SearchBar" class=smenu style="width:250" height=200>
  <table width=100% bgcolor="#aabbdd" cellspacing=0 cellpadding=1>
    <tr>
      <td colspan=2 bgcolor="#aabbdd">

        <table border=0  width="100%">
          <tr valign="top">
            <td colspan='2' align='left'>
                &nbsp;&nbsp;<input type='radio' name='printflag' value='1' checked>导出整张报表。<br>
                &nbsp;&nbsp;<input type='radio' name='printflag' value='0'>按导出设置导出报表。
                <br>
                <br>
                <br>
                <br>
            </td>
          </tr>
          <tr valign="top">
            <td width="64">
            </td>
            <td align="right">
              <input type="button" onclick="download('64864.htm','rptfile','1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)_2016年.xls','1-1&nbsp;&nbsp;行&nbsp;政&nbsp;区&nbsp;划&nbsp;(2015年末)');" value="确定" class="btnmenudoc" onmouseover="this.className='btnmenudocmouseover'" onmouseout="this.className='btnmenudoc'">
              <input type="button" onclick="Hide(SearchBar);" value="取消" class="btnmenudoc" onmouseover="this.className='btnmenudocmouseover'" onmouseout="this.className='btnmenudoc'">
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</div>
<iframe name="printPage" src="" width=0px class="iframe" height=0px  style="border:0"  FRAMEBORDER=0>
</iframe>
</body>
<script language='javascript' type="">

     if(ttab)
     {
      ttab.style.display="none";
     }

function preview()
{

     var bdhtml=printtab.rows[2].cells[0].innerHTML;
     bdhtml=bdhtml.substring(bdhtml.indexOf(">")+1,bdhtml.length);

     var dindex=bdhtml.indexOf("DISPLAY");
     if(dindex==-1)
     {
        dindex=bdhtml.indexOf("display");
     }
     if(dindex!=-1)
     {
       var hht=bdhtml.substring(0,dindex);
       bdhtml=bdhtml.substring(dindex,bdhtml.length);
       bdhtml=bdhtml.substring(bdhtml.indexOf(";")+1,bdhtml.length);
       bdhtml=hht+bdhtml;
     }
      var f=document.forms[0];
      window.document.all.printPage.focus();
      f.printtxt.value=bdhtml;
      f.action="/gzStat1/rpt/print.jsp";
      f.target="_blank";
      f.submit();

}

</script>
</html>

"""


soup = BeautifulSoup(html, 'lxml')

table = TableDataProcess(soup, 'test')

print(table)

