#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            """
            if question_type == 'university_major':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            """
            elif question_type == 'major_university':
                sql = self.sql_transfer(question_type, entity_dict.get('major'))
            """
            """
            elif question_type == 'university_province':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            #从elif改为if
            if question_type == 'province_university':
                sql = self.sql_transfer(question_type, entity_dict.get('province'))
            """
            elif question_type == 'university_score':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            """
            elif question_type == 'score_university':
                sql = self.sql_transfer(question_type, entity_dict.get('score'))
            """
            """
            elif question_type == 'university_985':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            """
            elif question_type == '985_university':
                sql = self.sql_transfer(question_type, entity_dict.get('985'))
            """
            """
            elif question_type == 'university_211':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            """
            elif question_type == '211_university':
                sql = self.sql_transfer(question_type, entity_dict.get('211'))
            """
            """
            elif question_type == 'university_doubleclass':
                sql = self.sql_transfer(question_type, entity_dict.get('university'))
            """
            """
            elif question_type == 'doubleclass_university':
                sql = self.sql_transfer(question_type, entity_dict.get('doubleclass'))
            """
            
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        
        # 
        #if question_type == 'university_major':
        #    sql = ["MATCH (m:university) where m.name = '{0}' return m.name, m.major".format(i) for i in entities]

        # 
        #elif question_type == 'major_university':
        #    sql = ["MATCH (m:major) where m.name = '{0}' return m.name, m.university".format(i) for i in entities]
        # 
        #elif question_type == 'university_province':
        #    sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.province".format(i) for i in entities]
        
        # sql来自图谱组提供的接口函数，elif改为if
        if question_type == 'province_university':
            sql = "MATCH (n:`学校`)-[:located]-(p:`省份`) WHERE p.Name='" + str(province)+ "' RETURN n"
        
        # 
        #elif question_type == 'university_score':
        #    sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.score".format(i) for i in entities]
        
        # 
        #elif question_type == 'score_university':
        #    sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.university".format(i) for i in entities]
        
        # 
        #elif question_type == 'university_985':
        #    sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.985".format(i) for i in entities]
        
        # 
        #elif question_type == '985_university':
        #    sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 
        #elif question_type == 'university_211':
        #    sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 
        #elif question_type == '211_university':
        #    sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #    sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #    sql = sql1 + sql2
        # 

        #elif question_type == 'university_doubleclass':
        #    sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
    
        #
        #elif question_type == 'doubleclass_university':
        #    sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #    sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #    sql = sql1 + sql2

        elif question_type == 'province_firstline':
            sql= None

        else:
            pass


        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
