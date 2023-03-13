use nienluan;
create table user(
	userName varchar(50) primary key,
    gmail varchar(50),
    pass varchar(20)
    );

create table exam(
	codeExam varchar(20) primary key,
    amount int
    );

create table answer(
	codeExam varchar(20),
    foreign key(codeExam) references exam(codeExam),
    answer varchar(5)
	);
    
create table student(
	codeStudent varchar(20) primary key,
    codeExam varchar(20),
    foreign key(codeExam) references exam(codeExam),
    score float
    );
    
create table project(
	projectname varchar(50) primary key,
    codeExam varchar(20),
    foreign key(codeExam) references exam(codeExam),
    username varchar(50),
    foreign key(username) references user(username),
    codeStudent varchar(20),
    foreign key(codeStudent) references student(codeStudent)
    );
    
